"""
File:           recipe_parser.py
Description:    Provides a class that takes text from a Jinja-formatted recipe file and parses it. This allows for easy
                semantic understanding and manipulation of the file.

                Patching these files is done using a JSON-patch like syntax. This project closely conforms to the
                RFC 6902 spec, but deviates in some specific ways to handle the Jinja variables and comments found in
                conda recipe files.

                Links:
                - https://jsonpatch.com/
                - https://datatracker.ietf.org/doc/html/rfc6902/
"""
# Allows older versions of python to use newer forms of type annotation. There are major features introduced in >=3.9
from __future__ import annotations

import ast
import difflib
import json
import re
from typing import Callable, Final, Optional

import yaml
from jsonschema import validate as schema_validate

from percy.parser._node import Node
from percy.parser._selector_info import SelectorInfo
from percy.parser._traverse import remap_child_indices_virt_to_phys, traverse, traverse_all, traverse_with_index
from percy.parser._types import (
    PERCY_SUB_MARKER,
    ROOT_NODE_VALUE,
    ForceIndentDumper,
    OpsTable,
    Regex,
    StrStack,
    StrStackImmutable,
)
from percy.parser._utils import num_tab_spaces, stack_path_to_str, str_to_stack_path, stringify_yaml, substitute_markers
from percy.parser.enums import SelectorConflictMode
from percy.parser.exceptions import JsonPatchValidationException
from percy.parser.types import (
    JSON_PATCH_SCHEMA,
    PRIMITIVES_TUPLE,
    TAB_AS_SPACES,
    TAB_SPACE_COUNT,
    JsonPatchType,
    JsonType,
    Primitives,
)


class RecipeParser:
    """
    Class that parses a recipe file string. Provides many useful mechanisms for changing values in the document.

    A quick search for Jinja statements in YAML files shows that the vast majority of statements are in the form of
    initializing variables with `set`.

    The next few prevalent kinds of statements are:
      - Conditional macros (i.e. if/endif)
      - for loops
    And even those only show up in a handful out of thousands of recipes. There are also no current examples of Jinja
    style comments.

    So that being said, the initial parser will not support these more edge-case recipes as they don't pass the 80/20
    rule.
    """

    # Static set of patch operations that require `value`. The others require `from`.
    _patch_ops_requiring_value = set(["add", "remove", "replace", "test"])
    # Sentinel object used for detecting defaulting behavior.
    # See here for a good explanation: https://peps.python.org/pep-0661/
    _sentinel = object()

    @staticmethod
    def _parse_yaml(s: str, parser: Optional[RecipeParser] = None) -> JsonType:
        """
        Parse a line (or multiple) of YAML into a Pythonic data structure
        :param s:       String to parse
        :param parser:  (Optional) If provided, this will substitute Jinja variables with values specified in in the
                        recipe file. Since `_parse_yaml()` is critical to constructing recipe files, this function must
                        remain static. Also, during construction, we shouldn't be using a variables until the entire
                        recipe is read/parsed.
        :return: Pythonic data corresponding to the line of YAML
        """

        # Recursive helper function used when we need to perform variable substitutions
        def _parse_yaml_recursive_sub(data: JsonType, modifier: Callable[[JsonType], JsonType]) -> JsonType:
            # Add the substitutions back in
            if isinstance(data, str):
                data = modifier(data)
            if isinstance(data, dict):
                for key in data.keys():
                    data[key] = _parse_yaml_recursive_sub(data[key], modifier)
            elif isinstance(data, list):
                for i in range(len(data)):
                    data[i] = _parse_yaml_recursive_sub(data[i], modifier)
            return data

        output: JsonType = None
        try:
            output = yaml.safe_load(s)
        except Exception:  # pylint: disable=broad-exception-caught
            # If a construction exception is thrown, attempt to re-parse by replacing Jinja macros (substrings in
            # `{{}}`) with friendly string substitution markers, then re-inject the substitutions back in. We classify
            # all Jinja substitutions as string values, so we don't have to worry about the type of the actual
            # substitution.
            sub_list = Regex.JINJA_SUB.findall(s)
            s = Regex.JINJA_SUB.sub(PERCY_SUB_MARKER, s)
            output = _parse_yaml_recursive_sub(yaml.safe_load(s), lambda d: substitute_markers(d, sub_list))
            # Because we leverage PyYaml to parse the data structures, we need to perform a second pass to perform
            # variable substitutions.
            if parser is not None:
                output = _parse_yaml_recursive_sub(
                    output, parser._render_jinja_vars  # pylint: disable=protected-access
                )

        return output

    @staticmethod
    def _parse_line_node(s: str) -> Node:
        """
        Parses a line of conda-formatted YAML into a Node.

        Latest YAML spec can be found here: https://yaml.org/spec/1.2.2/

        :param s:   Pre-stripped (no leading/trailing spaces), non-Jinja line of a recipe file
        :return: A Node representing a line of the conda-formatted YAML.
        """
        # Use PyYaml to safely/easily/correctly parse single lines of YAML.
        output = RecipeParser._parse_yaml(s)

        # Attempt to parse-out comments. Fully commented lines are not ignored to preserve context when the text is
        # rendered. Their order in the list of child nodes will preserve their location. Fully commented lines just have
        # a value of "None".
        #
        # There is an open issue to PyYaml to support comment parsing:
        #   - https://github.com/yaml/pyyaml/issues/90
        comment = ""
        # The full line is a comment
        if s.startswith("#"):
            return Node(comment=s)
        # There is a comment at the end of the line if a `#` symbol is found with leading whitespace before it. If it is
        # "touching" a character on the left-side, it is just part of a string.
        comment_re_result = Regex.DETECT_TRAILING_COMMENT.search(s)
        if comment_re_result is not None:
            # Group 0 is the whole match, Group 1 is the leading whitespace, Group 2 locates the `#`
            comment = s[comment_re_result.start(2) :]

        # If a dictionary is returned, we have a line containing a key and potentially a value. There should only be 1
        # key/value pairing in 1 line. Nodes representing keys should be flagged for handling edge cases.
        if isinstance(output, dict):
            children: list[Node] = []
            key = list(output.keys())[0]
            # If the value returned is None, there is no leaf node to set
            if output[key] is not None:
                # As the line is shared by both parent and child, the comment gets tagged to both.
                children.append(Node(output[key], comment))
            return Node(key, comment, children, key_flag=True)
        # If a list is returned, then this line is a listed member of the parent Node
        if isinstance(output, list):
            # The full line is a comment
            if s.startswith("#"):
                # Comments are list members to ensure indentation
                return Node(comment=comment, list_member_flag=True)
            # Special scenarios that can occur on 1 line:
            #   1. Lists can contain lists: - - foo -> [["foo"]]
            #   2. Lists can contain keys:  - foo: bar -> [{"foo": "bar"}]
            # And, of course, there can be n values in each of these collections on 1 line as well. Scenario 2 occurs in
            # multi-output recipe files so we need to support the scenario here.
            #
            # `PKG-3006` tracks an investigation effort into what we need to support for our purposes.
            if isinstance(output[0], dict):
                # Build up the key-and-potentially-value pair nodes first
                key_children: list[Node] = []
                key = list(output[0].keys())[0]
                if output[0][key] is not None:
                    key_children.append(Node(output[0][key], comment))
                key_node = Node(key, comment, key_children, key_flag=True)

                elem_node = Node(comment=comment, list_member_flag=True)
                elem_node.children.append(key_node)
                return elem_node
            return Node(output[0], comment, list_member_flag=True)
        # Other types are just leaf nodes. This is scenario should likely not be triggered given our recipe files don't
        # have single valid lines of YAML, but we cover this case for the sake of correctness.
        return Node(output, comment)

    @staticmethod
    def _generate_subtree(value: JsonType) -> list[Node]:
        """
        Given a value supported by JSON, use the RecipeParser to generate a list of child nodes. This effectively
        creates a new subtree that can be used to patch other parse trees.
        """
        # Multiline values can replace the list of children with a single multiline leaf node.
        if isinstance(value, str) and "\n" in value:
            return [
                Node(
                    value=value.splitlines(),
                    multiline_flag=True,
                )
            ]

        # For complex types, generate the YAML equivalent and build a new tree.
        if not isinstance(value, PRIMITIVES_TUPLE):
            # Although not technically required by YAML, we add the optional spacing for human readability.
            return RecipeParser(  # pylint: disable=protected-access
                yaml.dump(value, Dumper=ForceIndentDumper)
            )._root.children

        # Primitives can be safely stringified to generate a parse tree.
        return RecipeParser(str(stringify_yaml(value)))._root.children  # pylint: disable=protected-access

    def _render_jinja_vars(self, s: str) -> JsonType:
        """
        Helper function that replaces Jinja substitutions with their actual set values.
        :param s:    String to be re-rendered
        :return: The original value, augmented with Jinja substitutions. If substitutions have taken place, the type is
                 re-evaluated.
        """
        replacement = False
        # Search the string, replacing all substitutions we can recognize
        for match in Regex.JINJA_SUB.findall(s):
            lower_case = False
            # The regex guarantees the string starts and ends with double braces
            key = match[2:-2].strip()
            # A brief search through `aggregate` shows that `|lower` is a commonly used Jinja command. Few, if any,
            # other commands are used, as of writing. If others are found, we might need to support them here.
            lower_match = Regex.JINJA_FUNCTION_LOWER.search(key)
            if lower_match is not None:
                lower_case = True
                key = key.replace(lower_match.group(), "").strip()

            if key in self._vars_tbl:
                # Replace value as a string. Re-interpret the entire value before returning.
                value = str(self._vars_tbl[key])
                if lower_case:
                    value = value.lower()
                s = s.replace(match, value)
                replacement = True
        if replacement:
            return yaml.safe_load(s)
        return s

    def _rebuild_selectors(self) -> None:
        """
        Re-builds the selector look-up table. This table allows quick access to tree nodes that have a selector
        specified. This needs to be called when the tree or selectors are modified.
        """
        self._selector_tbl: dict[str, list[SelectorInfo]] = {}

        def _collect_selectors(node: Node, path: StrStackImmutable) -> None:
            # Ignore empty comments
            if not node.comment:
                return
            match = Regex.SELECTOR.search(node.comment)
            if match:
                selector = match.group(0)
                selector_info = SelectorInfo(node, path)
                if selector not in self._selector_tbl:
                    self._selector_tbl[selector] = [selector_info]
                else:
                    self._selector_tbl[selector].append(selector_info)

        traverse_all(self._root, _collect_selectors)

    def __init__(self, content: str):
        """
        Constructs a RecipeParser instance.
        :param content: conda-build formatted recipe file, as a single text
                        string.
        """
        # The initial, raw, text is preserved for diffing and debugging purposes
        self._init_content: Final[str] = content
        # Indicates if the original content has changed
        self._is_modified = False

        # Tracks Jinja variables set by the file
        self._vars_tbl: dict[str, JsonType] = {}
        # Find all the set statements and record the values
        for line in Regex.JINJA_SET_LINE.findall(self._init_content):
            key = line[line.find("set") + len("set") : line.find("=")].strip()
            value = line[line.find("=") + len("=") : line.find("%}")].strip()
            try:
                self._vars_tbl[key] = ast.literal_eval(value)
            except Exception:  # pylint: disable=broad-exception-caught
                self._vars_tbl[key] = value

        # Root of the parse tree
        self._root = Node(ROOT_NODE_VALUE)
        # Start by removing all Jinja lines. Then traverse line-by-line
        sanitized_yaml = Regex.JINJA_LINE.sub("", self._init_content)

        # Read the YAML line-by-line, maintaining a stack to manage the last owning node in the tree.
        node_stack: list[Node] = [self._root]
        # Relative depth is determined by the increase/decrease of indentation marks (spaces)
        cur_indent = 0
        last_node = node_stack[-1]

        # Iterate with an index variable, so we can handle multiline values
        line_idx = 0
        lines = sanitized_yaml.splitlines()
        num_lines = len(lines)
        while line_idx < num_lines:
            line = lines[line_idx]
            # Increment here, so that the inner multiline processing loop doesn't cause a skip of the line following the
            # multiline value.
            line_idx += 1
            # Ignore empty lines
            clean_line = line.strip()
            if clean_line == "":
                continue

            new_indent = num_tab_spaces(line)
            new_node = RecipeParser._parse_line_node(clean_line)
            # If the last node ended (pre-comments) with a |, reset the value to be a list of the following,
            # extra-indented strings
            if Regex.MULTILINE.match(line):
                # Per YAML spec, multiline statements can't be commented. In other words, the `#` symbol is seen as a
                # string character in multiline values.
                multiline_node = Node([], multiline_flag=True)
                multiline = lines[line_idx]
                multiline_indent = num_tab_spaces(multiline)
                # Add the line to the list once it is verified to be the next line to capture in this node. This means
                # that `line_idx` will point to the line of the next node, post-processing.
                while multiline_indent > new_indent:
                    multiline_node.value.append(multiline.strip())
                    line_idx += 1
                    multiline = lines[line_idx]
                    multiline_indent = num_tab_spaces(multiline)
                # The previous level is the key to this multi-line value, so we can safely reset it.
                new_node.children = [multiline_node]
            if new_indent > cur_indent:
                node_stack.append(last_node)
            elif new_indent < cur_indent:
                # Multiple levels of depth can change from line to line, so multiple stack nodes must be pop'd. Example:
                # foo:
                #   bar:
                #     fizz: buzz
                # baz: blah
                # TODO Figure out tab-depth of the recipe being read. 4 spaces is technically valid in YAML
                depth_to_pop = (cur_indent - new_indent) // TAB_SPACE_COUNT
                for _ in range(depth_to_pop):
                    node_stack.pop()
            cur_indent = new_indent
            # Look at the stack to determine the parent Node and then append the current node to the new parent.
            parent = node_stack[-1]
            parent.children.append(new_node)
            # Update the last node for the next line interpretation
            last_node = new_node

        # Now that the tree is built, construct a selector look-up table that tracks all the nodes that use a particular
        # selector. This will make it easier to.
        #
        # This table will have to be re-built or modified when the tree is modified with `patch()`.
        self._rebuild_selectors()

    @staticmethod
    def _str_tree_recurse(node: Node, depth: int, lines: list[str]) -> str:
        """
        Helper function that renders a parse tree as a text-based dependency tree. Useful for debugging.
        :param node:    Node of interest
        :param depth:   Current depth of the node
        :param lines:   Accumulated list of lines to text to render
        """
        spaces = TAB_AS_SPACES * depth
        branch = "" if depth == 0 else "|- "
        lines.append(f"{spaces}{branch}{node.short_str()}")
        for child in node.children:
            RecipeParser._str_tree_recurse(child, depth + 1, lines)

    def __str__(self) -> str:
        """
        Casts the parser into a string. Useful for debugging.
        :return: String representation of the recipe file
        """
        s = "--------------------\n"
        tree_lines: list[str] = []
        RecipeParser._str_tree_recurse(self._root, 0, tree_lines)
        s += "RecipeParser Instance\n"
        s += "- Variables Table:\n"
        s += json.dumps(self._vars_tbl, indent=TAB_AS_SPACES) + "\n"
        s += "- Selectors Table:\n"
        for key, val in self._selector_tbl.items():
            s += f"{TAB_AS_SPACES}{key}\n"
            for info in val:
                s += f"{TAB_AS_SPACES}{TAB_AS_SPACES}- {info}\n"
        s += f"- is_modified?: {self._is_modified}\n"
        s += "- Tree:\n" + "\n".join(tree_lines) + "\n"
        s += "--------------------\n"

        return s

    def __eq__(self, other: object) -> bool:
        """
        Checks if two recipe representations match entirely
        :param other:   Other recipe parser instance to check against.
        :return: True if both recipes contain the same current state. False otherwise.
        """
        if not isinstance(other, RecipeParser):
            raise TypeError
        return self.render() == other.render()

    def is_modified(self) -> bool:
        """
        Indicates if the recipe has been changed since construction.
        :return: True if the recipe has changed. False otherwise.
        """
        return self._is_modified

    def has_unsupported_statements(self) -> bool:
        """
        Runs a series of checks against the original recipe file.
        :return: True if the recipe has statements we do not currently support. False otherwise.
        """
        # TODO complete
        raise NotImplementedError

    @staticmethod
    def _render_tree(node: Node, depth: int, lines: list[str], parent: Optional[Node] = None) -> None:
        """
        Recursive helper function that traverses the parse tree to generate a file.
        :param node:    Current node in the tree
        :param depth:   Current depth of the recursion
        :param lines:   Accumulated list of lines in the recipe file
        :param parent:  (Optional) Parent node to the current node. Set by recursive calls only.
        """
        spaces = TAB_AS_SPACES * depth

        # Handle same-line printing
        if node.is_single_key():
            # Edge case: Handle a list containing 1 member
            if node.children[0].list_member_flag:
                lines.append(f"{spaces}{node.value}:  {node.comment}".rstrip())
                lines.append(
                    f"{spaces}{TAB_AS_SPACES}- "
                    f"{stringify_yaml(node.children[0].value, True)}  "
                    f"{node.children[0].comment}".rstrip()
                )
                return

            # Edge case: The first element of dictionary in a list has a list `- ` prefix. ubsequent keys in the
            # dictionary just have a tab.
            if parent is not None and parent.is_collection_element() and node == parent.children[0]:
                lines.append(
                    f"{TAB_AS_SPACES * (depth-1)}- {node.value}: "
                    f"{stringify_yaml(node.children[0].value)}  "
                    f"{node.children[0].comment}".rstrip()
                )
                return

            # Handle multi-line statements. In theory this will probably only ever be strings, but we'll try to account
            # for other types.
            #
            # By the language spec, # symbols do not indicate comments on multiline strings.
            if node.children[0].multiline_flag:
                lines.append(f"{spaces}{node.value}: |  {node.comment}".rstrip())
                for val_line in node.children[0].value:
                    lines.append(f"{spaces}{TAB_AS_SPACES}" f"{stringify_yaml(val_line, True)}".rstrip())
                return
            lines.append(
                f"{spaces}{node.value}: "
                f"{stringify_yaml(node.children[0].value)}  "
                f"{node.children[0].comment}".rstrip()
            )
            return

        depth_delta = 1
        # Don't render a `:` for the non-visible root node. Also don't render invisible collection nodes.
        if depth > -1 and not node.is_collection_element():
            list_prefix = ""
            # Being in a list changes how the depth is rendered
            if node.list_member_flag:
                depth_delta += 1
                list_prefix = "- "
            # Nodes representing collections in a list have nothing to render
            lines.append(f"{spaces}{list_prefix}{node.value}:  {node.comment}".rstrip())

        for child in node.children:
            # Top-level empty-key edge case: Top level keys should have no additional indentation.
            extra_tab = "" if depth < 0 else TAB_AS_SPACES
            # Comments in a list are indented to list-level, but do not include a list `-` mark
            if child.is_comment():
                lines.append(f"{spaces}{extra_tab}" f"{child.comment}".rstrip())
            # Empty keys can be easily confused for leaf nodes. The difference is these nodes render with a "dangling"
            # `:` mark
            elif child.is_empty_key():
                lines.append(f"{spaces}{extra_tab}" f"{stringify_yaml(child.value)}:  " f"{child.comment}".rstrip())
            # Leaf nodes are rendered as members in a list
            elif child.is_leaf():
                lines.append(
                    f"{spaces}{TAB_AS_SPACES}- " f"{stringify_yaml(child.value)}  " f"{child.comment}".rstrip()
                )
            else:
                RecipeParser._render_tree(child, depth + depth_delta, lines, node)
            # By tradition, recipes have a blank line after every top-level section, unless they are a comment. Comments
            # should be left where they are.
            if depth < 0 and not child.is_comment():
                lines.append("")

    def render(self) -> str:
        """
        Takes the current state of the parse tree and returns the recipe file as a string.
        :return: String representation of the recipe file
        """
        lines = []

        # Render variable set section
        for key, val in self._vars_tbl.items():
            # Double quote strings
            if isinstance(val, str):
                val = f'"{val}"'
            lines.append(f"{{% set {key} = {val} %}}")
        # Add spacing if variables have been set
        if len(self._vars_tbl):
            lines.append("")

        # Render parse-tree, -1 is passed in as the "root-level" is not directly rendered in a YAML file; it is merely
        # implied.
        RecipeParser._render_tree(self._root, -1, lines)

        return "\n".join(lines)

    @staticmethod
    def _render_object_tree(node: Node, replace_variables: bool, data: JsonType) -> None:
        """
        Recursive helper function that traverses the parse tree to generate a Pythonic data object.
        :param node:                Current node in the tree
        :param replace_variables:   If set to True, this replaces all variable substitutions with their set values.
        :param data:                Accumulated data structure
        """
        # Ignore comment-only lines
        if node.is_comment():
            return

        key = node.value
        for child in node.children:
            # Ignore comment-only lines
            if child.is_comment():
                continue

            # Handle multiline strings
            value = child.value if not child.multiline_flag else "\n".join(child.value)
            # TODO if enabled, string replace `{{}}` in `value`
            # TODO handle `| lower` and similar
            # TODO create new function for handling grammar
            if replace_variables:
                pass

            # Empty keys are interpreted to point to `None`
            if child.is_empty_key():
                data[key][child.value] = None
                continue

            # List members accumulate values in a list
            if child.list_member_flag:
                if key not in data:
                    data[key] = []
                data[key].append(value)
                continue

            # Other (non list and non-empty-key) leaf nodes set values directly
            if child.is_leaf():
                data[key] = value
                continue

            # All other keys prep for containing more dictionaries
            data.setdefault(key, {})
            RecipeParser._render_object_tree(child, replace_variables, data[key])

    def render_to_object(self, replace_variables: bool = False) -> JsonType:
        """
        Takes the underlying state of the parse tree and produces a Pythonic object/dictionary representation. Analogous
        to `json.load()`.
        :param replace_variables:   (Optional) If set to True, this replaces all variable substitutions with their set
                                    values.
        :return: Pythonic data object representation of the recipe.
        """
        data: JsonType = {}

        # Bootstrap/flatten the root-level
        for child in self._root.children:
            if child.is_comment():
                continue
            data.setdefault(child.value, {})
            RecipeParser._render_object_tree(child, replace_variables, data)

        return data

    ## YAML Access Functions ##

    def list_value_paths(self) -> list[str]:
        """
        Provides a list of all known terminal paths. This can be used by the caller to perform search operations.
        :return: List of all terminal paths in the parse tree.
        """
        lst: list[str] = []

        def _find_paths(node: Node, path_stack: StrStack) -> None:
            if node.is_leaf():
                lst.append(stack_path_to_str(path_stack))

        traverse_all(self._root, _find_paths)
        return lst

    def contains_value(self, path: str) -> bool:
        """
        Determines if a value (via a path) is contained in this recipe. This also allows the caller to determine if a
        path exists.
        :param path:    JSON patch (RFC 6902)-style path to a value.
        :return: True if the path exists. False otherwise.
        """
        path_stack = str_to_stack_path(path)
        return traverse(self._root, path_stack) is not None

    def get_value(self, path: str, default: JsonType = _sentinel, sub_vars: bool = False) -> JsonType:
        """
        Retrieves a value at a given path. If the value is not found, return a specified default value or throw.
        :param path:        JSON patch (RFC 6902)-style path to a value.
        :param default:     (Optional) If the value is not found, return this value instead.
        :param sub_vars:    (Optional) If set to True and the value contains a Jinja template variable, the Jinja value
                            will be "rendered".
        :raises KeyError: If the value is not found AND no default is specified
        :return: If found, the value in the recipe at that path. Otherwise, the caller-specified default value.
        """
        path_stack = str_to_stack_path(path)
        node = traverse(self._root, path_stack)

        # Handle if the path was not found
        if node is None:
            if default == RecipeParser._sentinel:
                raise KeyError(f"No value/key found at path {path!r}")
            return default

        return_value: JsonType = None
        # Handle unpacking of the last key-value set of nodes.
        if node.is_single_key() and not node.is_root():
            # As of writing, Jinja substitutions are not used
            if node.children[0].multiline_flag:
                # PyYaml will not preserve newlines passed into strings, so we can directly check for variable
                # substitutions on a multiline string
                multiline_str = "\n".join(node.children[0].value)
                if sub_vars:
                    return self._render_jinja_vars(multiline_str)
                return multiline_str
            return_value = node.children[0].value
        # Leaf nodes can return their value directly
        elif node.is_leaf():
            return_value = node.value
        else:
            # NOTE: Traversing the tree and generating our own data structures will be more efficient than rendering and
            # leveraging the YAML parser, BUT this method re-uses code and is easier to maintain.
            lst = []
            RecipeParser._render_tree(node, -1, lst)
            return_value = "\n".join(lst)

        # Collection types may contain strings that need to be re-rendered
        if isinstance(return_value, (list, dict, str)):
            parser = self if sub_vars else None
            return RecipeParser._parse_yaml(return_value, parser)
        return return_value

    def find_value(self, value: Primitives) -> list[str]:
        """
        Given a value, find all the paths that contain that value.

        NOTE: This only supports searching for "primitive" values, i.e. you cannot search for collections.

        :param value:   Value to find in the recipe.
        :raises ValueError: If the value provided is not a primitive type.
        :return: List of paths where the value can be found.
        """
        if not isinstance(value, PRIMITIVES_TUPLE):
            raise ValueError(f"A non-primitive value was provided: {value}")

        paths: list[str] = []

        def _find_value_paths(node: Node, path_stack: StrStack) -> None:
            # Special case: empty keys imply a null value, although they don't contain a null child.
            if (value is None and node.is_empty_key()) or (node.is_leaf() and node.value == value):
                paths.append(stack_path_to_str(path_stack))

        traverse_all(self._root, _find_value_paths)

        return paths

    ## Jinja Variable Functions ##

    def list_variables(self) -> list[str]:
        """
        Returns variables found in the recipe, sorted by first appearance.
        :return: List of variables found in the recipe.
        """
        return list(self._vars_tbl.keys())

    def contains_variable(self, var: str) -> bool:
        """
        Determines if a variable is set in this recipe.
        :param var: Variable to check for.
        :return: True if a variable name is found in this recipe. False otherwise.
        """
        return var in self._vars_tbl

    def get_variable(self, var: str, default: Primitives = _sentinel) -> Primitives:
        """
        Returns the value of a variable set in the recipe. If specified, a default value will be returned if the
        variable name is not found.
        :param var:     Variable of interest check for.
        :param default: (Optional) If the value is not found, return this value instead.
        :raises KeyError:   If the value is not found AND no default is specified
        :return: The value (or specified default value if not found) of the variable name provided.
        """
        if var not in self._vars_tbl:
            if default == RecipeParser._sentinel:
                raise KeyError
            return default
        return self._vars_tbl[var]

    def set_variable(self, var: str, value: Primitives) -> None:
        """
        Adds or changes an existing Jinja variable.
        :param var:     Variable to modify
        :param value:   Value to set
        """
        self._vars_tbl[var] = value
        self._is_modified = True

    def del_variable(self, var: str) -> None:
        """
        Remove a variable from the project. If one is not found, no changes are made.
        :param var: Variable to delete
        """
        if not var in self._vars_tbl:
            return
        del self._vars_tbl[var]
        self._is_modified = True

    def get_variable_references(self, var: str) -> list[str]:
        """
        Returns a list of paths that use particular variables.
        :param var: Variable of interest
        :return: List of paths that use a variable, sorted by first appearance.
        """
        if var not in self._vars_tbl:
            return []

        path_list: list[str] = []
        # The text between the braces is very forgiving. Just searching for whitespace characters means we will never
        # match the very common `{{ name | lower }}` expression, or similar piping functions.
        var_re = re.compile(r"{{.*" + var + r".*}}")

        def _collect_var_refs(node: Node, path: StrStackImmutable) -> None:
            # Variables can only be found inside string values.
            if isinstance(node.value, str) and var_re.search(node.value):
                path_list.append(stack_path_to_str(path))

        traverse_all(self._root, _collect_var_refs)
        # The list should be de-duped and maintain order.
        return list(dict.fromkeys(path_list))

    ## Selector Functions ##

    def list_selectors(self) -> list[str]:
        """
        Returns selectors found in the recipe, sorted by first appearance.
        :return: List of selectors found in the recipe.
        """
        return list(self._selector_tbl.keys())

    def contains_selector(self, selector: str) -> bool:
        """
        Determines if a selector expression is present in this recipe.
        :param selector:    Selector to check for.
        :return: True if a selector is found in this recipe. False otherwise.
        """
        return selector in self._selector_tbl

    def get_selector_paths(self, selector: str) -> list[str]:
        """
        Given a selector (including the surrounding brackets), provide a list of paths in the parse tree that use that
        selector.

        Selector paths will be ordered by the line they appear on in the file.

        :param selector:    Selector of interest.
        :return: A list of all known paths that use a particular selector
        """
        # We return a tuple so that caller doesn't accidentally modify a private member variable.
        if not self.contains_selector(selector):
            return []
        path_list: list[str] = []
        for path_stack in self._selector_tbl[selector]:
            path_list.append(stack_path_to_str(path_stack.path))
        # The list should be de-duped and maintain order. Duplications occur when key-value pairings mean a selector
        # occurs on two nodes with the same path.
        #
        # For example:
        #   skip: True  # [unix]
        # The nodes for both `skip` and `True` contain the comment `[unix]`
        return list(dict.fromkeys(path_list))

    def add_selector(self, path: str, selector: str, mode: SelectorConflictMode = SelectorConflictMode.REPLACE) -> None:
        """
        Given a path, add a selector (include the surrounding brackets) to the line denoted by path.
        :param path:        Path to add a selector to
        :param selector:    Selector statement to add
        :param mode:        (Optional) Indicates how to handle a conflict if a selector already exists at this path.
        :raises KeyError:   If the path provided is not found
        :raises ValueError: If the selector provided is malformed
        """
        path_stack = str_to_stack_path(path)
        node = traverse(self._root, path_stack)

        if node is None:
            raise KeyError(f"Path not found: {path!r}")
        if not Regex.SELECTOR.match(selector):
            raise ValueError(f"Invalid selector provided: {selector}")

        # Helper function that extracts the outer set of []'s in a selector
        def _extract_selector(s: str) -> str:
            return s.replace("[", "", 1)[::-1].replace("]", "", 1)[::-1]

        comment = ""
        old_selector_found = Regex.SELECTOR.search(node.comment)
        if node.comment == "" or mode == SelectorConflictMode.REPLACE:
            comment = f"# {selector}"
        # "Append" to existing selectors
        elif old_selector_found:
            logic_op = "and" if mode == SelectorConflictMode.AND else "or"
            old_selector = _extract_selector(old_selector_found.group())
            new_selector = _extract_selector(selector)
            comment = f"# [{old_selector} {logic_op} {new_selector}]"
        # If the comment is not a selector, put the selector first, then append the comment.
        else:
            # Strip the existing comment of it's leading `#` symbol
            comment = f"# {selector} {node.comment.replace('#', '', 1).strip()}"

        node.comment = comment
        # Some lines of YAML correspond to multiple nodes. For consistency, we need to ensure that comments are
        # duplicate across all nodes on a line.
        if node.is_single_key():
            node.children[0].comment = comment

        self._rebuild_selectors()
        self._is_modified = True

    def remove_selector(self, path: str) -> Optional[str]:
        """
        Given a path, remove a selector to the line denoted by path.
        - If a selector does not exist, nothing happens.
        - If a comment exists after the selector, keep it, discard the selector.
        :param path:        Path to add a selector to
        :raises KeyError:   If the path provided is not found
        :return: If found, the selector removed (includes surrounding brackets). Otherwise, returns None
        """
        path_stack = str_to_stack_path(path)
        node = traverse(self._root, path_stack)

        if node is None:
            raise KeyError(f"Path not found: {path!r}")

        search_results = Regex.SELECTOR.search(node.comment)
        if not search_results:
            return None

        selector = search_results.group(0)
        comment = node.comment.replace(selector, "")
        # Sanitize potential edge-case scenarios after a removal
        comment = comment.replace("#  ", "# ").replace("# # ", "# ")
        # Detect and remove empty comments. Other comments should remain intact.
        if comment.strip() == "#":
            comment = ""

        node.comment = comment
        # Some lines of YAML correspond to multiple nodes. For consistency, we need to ensure that comments are
        # duplicate across all nodes on a line.
        if node.is_single_key():
            node.children[0].comment = comment

        self._rebuild_selectors()
        self._is_modified = True
        return selector

    ## YAML Patching Functions ##

    @staticmethod
    def _is_valid_patch_node(node: Node, node_idx: int) -> bool:
        """
        Indicates if the target node to perform a patch operation against is a valid node. This is based on the RFC spec
        for JSON patching paths.
        :param node:        Target node to validate
        :param node_idx:    If the caller is evaluating that a list member, exists, this is the index into that list.
                            Otherwise this value should be less than 0.
        :return: True if the node can be patched. False otherwise.
        """
        # Path not found
        if node is None:
            return False

        # Leaf nodes contain values and not path information. Paths should not be made that access leaf nodes, with the
        # exception of members of a list and keys. Making such a path violates the RFC.
        if not node.list_member_flag and not node.key_flag and node.is_leaf():
            return False

        if node_idx >= 0:
            # You cannot use the list access feature to access non-lists
            if len(node.children) and not node.children[0].list_member_flag:
                return False
            # Check the bounds if the target requires the use of an index, remembering to use the virtual look-up table.
            idx_map = remap_child_indices_virt_to_phys(node.children)
            if node_idx > (len(idx_map) - 1):
                return False

        return True

    def _patch_add_find_target(self, path_stack: StrStack) -> tuple[Optional[Node], int, str, bool]:
        """
        Finds the target node of an `add()` operation, along with some supporting information.

        This function does not modify the parse tree.
        :param path_stack:  Path that describes a location in the tree, as a list, treated like a stack.
        :return: A tuple containing:
                   - The target node, if found (or the parent node if the target is a list member)
                   - The index of a node if the target is a list member
                   - An additional path that needs to be created, if applicable
                   - A flag indicating if the new data will be appended to a list
        """
        if len(path_stack) == 0:
            return None, -1, "", False

        # Special case that only applies to `add`. The `-` character indicates the new element can be added to the end
        # of the list.
        append_to_list = False
        if path_stack[0] == "-":
            path_stack.pop(0)
            append_to_list = True

        path_stack_copy = path_stack.copy()
        node, node_idx = traverse_with_index(self._root, path_stack)
        # Attempt to run a second time, if no node is found. As per the RFC, the containing object/list must exist. That
        # allows us to create only 1 level in the path.
        path_to_create = ""
        if node is None:
            path_to_create = path_stack_copy.pop(0)
            node, node_idx = traverse_with_index(self._root, path_stack_copy)

        return node, node_idx, path_to_create, append_to_list

    def _patch_add(self, _: str, path_stack: StrStack, value: JsonType) -> bool:
        """
        Performs a JSON patch `add` operation.
        :param path_stack:  Path that describes a location in the tree, as a list, treated like a stack.
        :param value:       Value to add.
        """
        # NOTE from the RFC:
        #   Because this operation is designed to add to existing objects and arrays, its target location will often
        #   not exist...However, the object itself or an array containing it does need to exist
        # In other words, the patch op will, at most, create 1 new path level. In addition, that also implies that
        # trying to append to an existing list only applies if the append operator is at the end of the list.
        node, node_idx, path_to_create, append_to_list = self._patch_add_find_target(path_stack)

        if not RecipeParser._is_valid_patch_node(node, node_idx):
            return False

        # If we couldn't find 1 level in the path, ensure that we re-insert that as the "root" of the sub-tree we are
        # about to create.
        if path_to_create:
            value = {path_to_create: value}

        new_children: Final[list[Node]] = RecipeParser._generate_subtree(value)
        # Mark children as list members if they are list members
        if append_to_list or node_idx >= 0:
            for child in new_children:
                child.list_member_flag = True

        # Insert members if an index is specified. Otherwise, extend the list of child nodes from the existing list.
        if node_idx >= 0:
            node.children[node_idx:node_idx] = new_children
        # Extend the list of children if we're appending or adding a new key.
        elif append_to_list or path_to_create:
            node.children.extend(new_children)
        # NOTE from the RFC: "If the member already exists, it is replaced by the specified value."
        else:
            node.children = new_children

        return True

    def _patch_remove(
        self, _0: str, path_stack: StrStack, _1: Optional[JsonType]  # pylint: disable=invalid-name
    ) -> bool:
        """
        Performs a JSON patch `remove` operation.
        :param path_stack:  Path that describes a location in the tree, as a list, treated like a stack.
        """
        if len(path_stack) == 0:
            return False

        # Removal in all scenarios requires targeting the parent node.
        node_idx = -1 if not path_stack[0].isdigit() else int(path_stack[0])
        # `traverse()` is destructive to the stack, so make a copy for the second traversal call.
        path_stack_copy = path_stack.copy()
        node_to_rm = traverse(self._root, path_stack)
        path_stack_copy.pop(0)
        node = traverse(self._root, path_stack_copy)

        if not RecipeParser._is_valid_patch_node(node_to_rm, -1) or not RecipeParser._is_valid_patch_node(
            node, node_idx
        ):
            return False

        if node_idx >= 0:
            # Pop the "physical" index, not the "virtual" one to ensure comments have been accounted for.
            node.children.pop(remap_child_indices_virt_to_phys(node.children)[node_idx])
            return True

        # In all other cases, the node to be removed must be found before eviction
        for i in range(len(node.children)):
            if node.children[i] == node_to_rm:
                node.children.pop(i)
                return True
        return False

    def _patch_replace(self, _: str, path_stack: StrStack, value: JsonType) -> bool:
        """
        Performs a JSON patch `replace` operation.
        :param path_stack:  Path that describes a location in the tree, as a list, treated like a stack.
        :param value:       Value to update with.
        """
        node, node_idx = traverse_with_index(self._root, path_stack)
        if not RecipeParser._is_valid_patch_node(node, node_idx):
            return False

        new_children: Final[list[Node]] = RecipeParser._generate_subtree(value)
        # Lists inject all children at the target position.
        if node_idx >= 0:
            # Ensure all children are marked as list members
            for child in new_children:
                child.list_member_flag = True
            node.children[node_idx:node_idx] = new_children
            # Evict the old child, which is now behind the new children
            node.children.pop(node_idx + len(new_children))
            return True

        # Leafs that represent values/paths of values can evict all children, and be replaced with new children, derived
        # from a new tree of values.
        node.children = new_children
        return True

    def _patch_move(self, path: str, path_stack: StrStack, value_from: JsonType) -> bool:
        """
        Performs a JSON patch `add` operation.
        :param path:        Path as a string.
        :param path_stack:  Path that describes a location in the tree, as a list, treated like a stack.
        :param value_from:  The "from" value in the JSON payload, i.e. the path the value originates from.
        """
        # NOTE from the RFC:
        #   This operation is functionally identical to a "remove" operation on the "from" location, followed
        #   immediately by an "add" operation at the target location with the value that was just removed.
        # So to save on development and maintenance, that is how this op is written.
        original_value: JsonType
        try:
            original_value = self.get_value(value_from)
        except KeyError:
            return False

        # Validate that `add`` will succeed before we `remove` anything
        node, node_idx, _, _ = self._patch_add_find_target(path_stack.copy())
        if not RecipeParser._is_valid_patch_node(node, node_idx):
            return False

        return self._patch_remove(value_from, str_to_stack_path(value_from), None) and self._patch_add(
            path, path_stack, original_value
        )

    def _patch_copy(self, path: str, path_stack: StrStack, value_from: JsonType) -> bool:
        """
        Performs a JSON patch `add` operation.
        :param path:        Path as a string.
        :param path_stack:  Path that describes a location in the tree, as a
                            list, treated like a stack.
        :param value_from:  The "from" value in the JSON payload, i.e. the
                            path the value originates from.
        """
        # NOTE from the RFC:
        #   This operation is functionally identical to an "add" operation at the target location using the value
        #   specified in the "from" member.
        # So to save on development and maintenance, that is how this op is written.
        original_value: JsonType
        try:
            original_value = self.get_value(value_from)
        except KeyError:
            return False

        return self._patch_add(path, path_stack, original_value)

    def _patch_test(self, path: str, _: StrStack, value: JsonType) -> bool:
        """
        Performs a JSON patch `test` operation.
        :param path:    Path as a string. Useful for invoking public class members.
        :param value:   Value to evaluate against.
        """
        try:
            return self.get_value(path) == value
        except KeyError:
            # Path not found
            return False

    def _get_supported_patch_ops(self) -> OpsTable:
        """
        Generates a look-up table of currently supported JSON patch operation functions, on this instance. This makes it
        easier to determine which operations are currently available AND simplifies "switch"-like logic.
        """
        return {
            "add": self._patch_add,
            "remove": self._patch_remove,
            "replace": self._patch_replace,
            "move": self._patch_move,
            "copy": self._patch_copy,
            "test": self._patch_test,
        }

    def patch(self, patch: JsonPatchType) -> bool:
        """
        Given a JSON-patch object, perform a patch operation.

        Modifications from RFC 6902
          - We're using a Jinja-formatted YAML file, not JSON
          - To modify variables, specify the variable name using `variable` not `path`. `path` implies lines in the file
          - To modify comments, specify the `path` AND `comment`

        Operations not currently supported:
          - add
          - remove
          - replace
          - move
          - copy
          - test

        :param patch:                           JSON-patch payload to operate with.
        :raises JsonPatchValidationException:   If the JSON-patch payload does not conform to our schema/spec.
        :return: If the calling code attempts to perform the `test` operation, this indicates the return value of the
                 `test` request. In other words, if `value` matches the target variable, return True. False otherwise.
        """
        # Validate the patch schema
        try:
            schema_validate(patch, JSON_PATCH_SCHEMA)
        except Exception as e:
            raise JsonPatchValidationException(patch) from e

        path: Final[str] = patch["path"]
        path_stack: Final[StrStack] = str_to_stack_path(path)

        # All RFC ops are supported, so the JSON schema validation checks will prevent us from getting this far, if
        # there is an issue.
        op: Final[str] = patch["op"]
        supported_patch_ops: Final[OpsTable] = self._get_supported_patch_ops()

        # The supplemental field name is determined by the operation type.
        value_from: Final[str] = "value" if op in RecipeParser._patch_ops_requiring_value else "from"

        # A no-op move is silly, but we might as well make it efficient AND ensure a no-op move doesn't corrupt our
        # modification flag.
        if op == "move" and path == patch[value_from]:
            return True

        # Both versions of the path are sent over so that the op can easily use both private and public functions
        # (without incurring even more conversions between path types). NOTE: The `remove` op has no `value` or `from`
        # field to pass in.
        is_successful = supported_patch_ops[op](path, path_stack, None if op == "remove" else patch[value_from])

        # Update the selector table and modified flag, if the operation succeeded.
        if is_successful and op != "test":
            # TODO this is not the most efficient way to update the selector table, but for now, it works.
            self._rebuild_selectors()
            # TODO technically this doesn't handle a no-op.
            self._is_modified = True

        return is_successful

    def search(self, regex: str, include_comment: bool = False) -> list[str]:
        """
        Given a regex string, return the list of paths that match the regex.
        NOTE: This function only searches against primitive values. All variables and selectors can be fully provided by
              using their respective `list_*()` functions.

        :param regex:           Regular expression to match with
        :param include_comment: (Optional) If set to `True`, this function will execute the regular expression on values
                                WITH their comments provided. For example: `42  # This is a comment`
        :return: Returns a list of paths where the matched value was found.
        """
        re_obj = re.compile(regex)
        paths: list[str] = []

        def _search_paths(node: Node, path_stack: StrStack) -> None:
            value = str(stringify_yaml(node.value))
            if include_comment and node.comment:
                value = f"{value}{TAB_AS_SPACES}{node.comment}"
            if node.is_leaf() and re_obj.search(value):
                paths.append(stack_path_to_str(path_stack))

        traverse_all(self._root, _search_paths)

        return paths

    def search_and_patch(self, regex: str, patch: JsonPatchType, include_comment: bool = False) -> bool:
        """
        Given a regex string and a JSON patch, apply the patch to any values that match the search expression.
        :param regex:           Regular expression to match with
        :param patch:           JSON patch to perform. NOTE: The `path` field will be replaced with the path(s) found,
                                so it does not need to be provided.
        :param include_comment: (Optional) If set to `True`, this function will execute the regular expression on values
                                WITH their comments provided. For example: `42  # This is a comment`
        :return: Returns a list of paths where the matched value was found.
        """
        paths = self.search(regex, include_comment)
        summation: bool = True
        for path in paths:
            patch["path"] = path
            summation = summation and self.patch(patch)
        return summation

    def diff(self) -> str:
        """
        Returns a git-like-styled diff of the current recipe state with original state of the recipe. Useful for
        debugging and providing users with some feedback.
        :return: User-friendly displayable string that represents notifications made to the recipe.
        """
        if not self.is_modified():
            return ""
        # Utilize `difflib` to lower maintenance overhead.
        return "\n".join(
            difflib.unified_diff(
                self._init_content.splitlines(), self.render().splitlines(), fromfile="original", tofile="current"
            )
        )