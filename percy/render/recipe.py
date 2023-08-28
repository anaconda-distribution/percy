"""Recipe renderer.

Not as accurate as conda-build render, but faster and architecture independent.
"""

# TODO: refactor long lines and remove the following linter mute
# ruff: noqa: E501

import sys
import re
import itertools
import logging
from copy import deepcopy
from typing import Any, Dict, List, Set, TextIO
from pathlib import Path
from dataclasses import dataclass, field
from urllib.parse import urlparse
import jsonschema

from percy.render.variants import read_conda_build_config, Variant
from percy.render.exceptions import EmptyRecipe, MissingMetaYaml
import percy.render._renderer as renderer
from percy.render._renderer import RendererType
import percy.render._dumper as dumper


class Recipe:
    """Represents a recipe (meta.yaml) in editable form

    Using conda-build to render recipe is slow and a one-way
    process. We need to be able to load **and** save recipes, which is
    handled by the representation in this class.

    Recipes undergo two manipulation rounds before parsed as YAML:
     1. Selecting lines using ``# [expression]``
     2. Rendering as Jinja2 template

    Args:
        recipe_file (Path): Path to meta.yaml
        variant_id (str): configuration id
        variant (Variant): Variant configuration
        backend (RendererType, optional): Renderer backend.

    Attributes:
        recipe_file (Path): The recipe file
        recipe_dir (Path): The recipe directory
        variant_id (str): configuration id
        selector_dict (Variant): Variant configuration
        meta (Dict[str, Any]): Rendered recipe in as a dictionary
        skip (bool): Whether this variant is skipped.
        packages (Dict[str:Package]): Rendered Packages.
        meta_yaml (List[str]): Lines of the raw recipe file
        orig (Recipe): Original recipe before modifications
    """

    # patch schema
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "op": {"enum": ["add", "replace", "remove"]},
                "path": {"type": "string"},
                "match": {"type": "string"},
                "value": {
                    "type": ["string", "integer", "boolean", "array"],
                    "items": {"type": "string"}
                },
                "description": {"type": "string"},
            },
            "required": [
                "op",
                "path",
            ],
            "additionalProperties": False,
        },
    }

    def __init__(
        self,
        recipe_file: Path,
        variant_id: str = None,
        variant: Variant = None,
        renderer: RendererType = None,
    ):
        """Constructor

        Args:
            recipe_file (Path): Path to meta.yaml
            variant_id (str): configuration id
            variant (Variant): Variant configuration
        """
        #: recipe dir
        if recipe_file:
            self.recipe_file = recipe_file
            self.recipe_dir = recipe_file.parent
        else:
            self.recipe_file = ""
            self.recipe_dir = ""

        #: Selectors configuration
        if not variant_id:
            variant_id = "empty_variant"
        if not variant:
            variant = {}
        self.variant_id = variant_id
        self.selector_dict: Dict[str, Any] = variant

        #: render configuration
        self.renderer = renderer
        if not self.renderer:
            self.renderer = RendererType.PYYAML

        # Filled in by render()
        #: Parsed recipe YAML
        self.meta: Dict[str, Any] = {}
        self.skip = False
        self.packages: Dict[str:Package] = dict()

        # These will be filled in by _load_from_string()
        #: Lines of the raw recipe file
        self.meta_yaml: List[str] = []
        #: Original recipe before modifications (updated by _load_from_string)
        self.orig: Recipe = deepcopy(self)

    @property
    def path(self):
        """Full path to ``meta.yaml``"""
        return self.recipe_file

    @property
    def dir(self):
        """Path to recipe folder"""
        return self.recipe_dir

    def __str__(self) -> str:
        return str(self.recipe_dir)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} "{self.recipe_dir}"'

    def _load_from_string(self, data: str) -> "Recipe":
        """Load and `render` recipe contents from disk

        Args:
            data (str): raw meta.yaml as string.

        Raises:
            EmptyRecipe: The recipe is empty

        Returns:
            Recipe: This recipe object.
        """
        self.meta_yaml = data.splitlines()
        if not self.meta_yaml:
            raise EmptyRecipe(self)
        self.render()
        return self

    @classmethod
    def from_string(
        cls,
        recipe_text: str,
        variant_id: str = None,
        variant: Variant = None,
        return_exceptions: bool = False,
        renderer: RendererType = None,
    ) -> "Recipe":
        """Create new `Recipe` object from string

        Args:
            recipe_text (str): A raw recipe as a string.
            variant_id (str): Variant id
            variant (Variant): Variant configuration.
            return_exceptions (bool, optional): Whether to return exceptions. Defaults to False.
            renderer (RendererType, optional): Renderer backend. Defaults to PYYAML.

        Raises:
            MissingMetaYaml: Missing meta.yaml
            Exception: An exception

        Returns:
            Recipe: A Recipe object.
        """
        try:
            recipe = cls("", variant_id, variant, renderer)
            recipe._load_from_string(recipe_text)
        except Exception as exc:
            if return_exceptions:
                return exc
            raise exc
        recipe._set_original()
        return recipe

    @classmethod
    def from_file(
        cls,
        recipe_fname: str,
        variant_id: str = None,
        variant: Variant = None,
        return_exceptions: bool = False,
        renderer: RendererType = None,
    ) -> "Recipe":
        """Create new `Recipe` object from file

        Args:
            recipe_fname (str): Path to recipe meta.yaml
            variant_id (str): Variant id
            variant (Variant): Variant configuration.
            return_exceptions (bool, optional): Whether to return exceptions. Defaults to False.
            renderer (RendererType, optional): Renderer backend. Defaults to PYYAML.

        Raises:
            MissingMetaYaml: Missing meta.yaml
            Exception: An exception

        Returns:
            Recipe: A Recipe object.
        """
        recipe_fname = Path(recipe_fname)
        recipe = cls(recipe_fname, variant_id, variant, renderer)
        try:
            if recipe_fname.is_file():
                with open(recipe_fname) as text:
                    recipe._load_from_string(text.read())
        except FileNotFoundError:
            exc = MissingMetaYaml(recipe_fname)
            if return_exceptions:
                return exc
            raise exc
        except Exception as exc:
            if return_exceptions:
                return exc
            raise exc
        recipe._set_original()
        return recipe

    def save(self):
        """Save recipe dump to file"""
        with open(self.path, "w", encoding="utf-8") as fdes:
            fdes.write(self.dump())

    def _set_original(self) -> None:
        """Store the current state of the recipe as "original" version"""
        self.orig = deepcopy(self)

    def is_modified(self) -> bool:
        """Has recipe been modified.

        Returns:
            bool: True if recipe has been modified.
        """
        return self.meta_yaml != self.orig.meta_yaml

    def dump(self):
        """Dump recipe content"""
        return "\n".join(self.meta_yaml) + "\n"

    def render(self) -> None:
        """Convert recipe text into data structure

        - create jinja template from recipe content
        - render template
        - parse yaml
        - normalize
        """

        # re-init
        self.meta: Dict[str, Any] = {}
        self.skip = False
        self.packages: Dict[str:Package] = dict()

        # render meta.yaml
        self.meta = renderer.render(
            self.recipe_dir, self.dump(), self.selector_dict, self.renderer
        )

        # should this be skipped?
        bld = self.meta.get("build", {})
        if bld and bld.get("skip", False):
            self.skip = True

        # extract package info
        if not self.skip:
            self._render_packages()

    def _render_packages(self):
        def get_group_from_dev_url(meta, default):
            if not meta:
                return default
            try:
                dev_url = str(meta.get("about", {}).get("dev_url", "") or "").strip()
            except AttributeError:
                dev_url = ""
            if dev_url:
                org = next(iter(urlparse(dev_url).path.lstrip("/").split("/")), "")
                org = str(org or "").strip().lower()
                if org:
                    return org
            else:
                return default

        # read main package deps
        name = self.meta.get("package", {}).get("name", "unknown").strip()
        version = str(self.meta.get("package", {}).get("version", "-1")).strip()
        number = str(dict(self.meta.get("build", {}) or {}).get("number", "0")).strip()
        group = get_group_from_dev_url(self.meta, name)
        path_prefix = ""
        is_noarch = False
        run_exports = []
        ignore_run_exports = []
        main_build = self.meta.get("build", {})
        if main_build:
            is_noarch = main_build.get("noarch", False)
            run_exports = main_build.get("run_exports", [])
            if not run_exports:
                run_exports = []
            run_exports = [
                Dep(i, "build/run_exports")
                for i in run_exports
                if (
                    i is not None
                    and i not in ["noarch", "strong", "weak"]
                    and str(i).strip()
                )
            ]
            ignore_run_exports = main_build.get("ignore_run_exports", [])
            if not ignore_run_exports:
                ignore_run_exports = []
        pkg_reqs = {"build": [], "host": [], "run": [], "run_constrained": []}
        requirements = self.meta.get("requirements", {})
        if requirements is not None:
            if isinstance(requirements, list):
                pkg_reqs["run"].extend(requirements)
            else:
                for s in pkg_reqs.keys():
                    reqs = requirements.get(s, [])
                    if reqs is not None:
                        if isinstance(reqs, list):
                            pkg_reqs[s].extend(reqs)
                        else:
                            pkg_reqs[s].extend([reqs])
            for s in pkg_reqs.keys():
                pkg_reqs[s] = [
                    Dep(i, f"requirements/{s}")
                    for i in pkg_reqs[s]
                    if (i is not None and str(i).strip())
                ]
        test = self.meta.get("test", {})
        test_reqs = []
        if test is not None:
            if isinstance(test, dict):
                reqs = test.get("requires", [])
                if reqs is not None:
                    if isinstance(reqs, list):
                        test_reqs.extend(reqs)
                    else:
                        test_reqs.extend([reqs])
            test_reqs = [
                Dep(i, "test/requires")
                for i in test_reqs
                if (i is not None and str(i).strip())
            ]
        if not self.meta.get("outputs", []):
            # only add if not a multi output recipe
            self.packages[name] = Package(
                self,
                name,
                version,
                number,
                group,
                set(pkg_reqs["build"]),
                set(pkg_reqs["host"]),
                set(pkg_reqs["run"]),
                set(pkg_reqs["run_constrained"]),
                set(run_exports),
                set(ignore_run_exports),
                set(test_reqs),
                is_noarch,
                path_prefix,
            )

        # read output package deps
        outputs = self.meta.get("outputs", [])
        if outputs:
            for n, output in enumerate(outputs):
                name = output.get("name", "")
                version = str(output.get("version", version)).strip()
                group = get_group_from_dev_url(output, group)
                path_prefix = f"outputs/{n}/"
                is_noarch = False
                run_exports = []
                ignore_run_exports = []
                main_build = output.get("build", {})
                if main_build:
                    number = str(main_build.get("number", number) or number).strip()
                    is_noarch = main_build.get("noarch", False)
                    run_exports = main_build.get("run_exports", [])
                    if not run_exports:
                        run_exports = []
                    run_exports = [
                        Dep(i, f"outputs/{n}/run_exports")
                        for i in run_exports
                        if (
                            i is not None
                            and i not in ["noarch", "strong", "weak"]
                            and str(i).strip()
                        )
                    ]
                    ignore_run_exports = main_build.get("ignore_run_exports", [])
                    if not ignore_run_exports:
                        ignore_run_exports = []
                output_pkg_reqs = deepcopy(pkg_reqs)
                requirements = output.get("requirements", {})
                if requirements is not None:
                    if isinstance(requirements, list):
                        output_pkg_reqs["run"].extend(requirements)
                    else:
                        for s in pkg_reqs.keys():
                            reqs = requirements.get(s, [])
                            if reqs is not None:
                                if isinstance(reqs, list):
                                    output_pkg_reqs[s].extend(reqs)
                                else:
                                    output_pkg_reqs[s].extend([reqs])
                    for s in output_pkg_reqs.keys():
                        output_pkg_reqs[s] = [
                            Dep(i, f"outputs/{n}/requirements/{s}")
                            for i in output_pkg_reqs[s]
                            if (i is not None and str(i).strip())
                        ]
                test = output.get("test", {})
                test_reqs = []
                if test is not None:
                    if isinstance(test, dict):
                        reqs = test.get("requires", [])
                        if reqs is not None:
                            if isinstance(reqs, list):
                                test_reqs.extend(reqs)
                            else:
                                test_reqs.extend([reqs])
                    test_reqs = [
                        Dep(i, f"outputs/{n}/test/requires")
                        for i in test_reqs
                        if (i is not None and str(i).strip())
                    ]
                self.packages[name] = Package(
                    self,
                    name,
                    version,
                    number,
                    group,
                    set(output_pkg_reqs["build"]),
                    set(output_pkg_reqs["host"]),
                    set(output_pkg_reqs["run"]),
                    set(output_pkg_reqs["run_constrained"]),
                    set(run_exports),
                    set(ignore_run_exports),
                    set(test_reqs),
                    is_noarch,
                    path_prefix,
                )

    def __getitem__(self, key):
        return self.meta[key]

    def _walk(self, path, noraise=False):
        nodes = [self.meta]
        keys = []
        for key in path.split("/"):
            last = nodes[-1]
            if key.isdigit():
                number = int(key)
                if isinstance(last, list):
                    if noraise and len(last) < number:
                        break
                    nodes.append(last[number])
                    keys.append(number)
                    continue
                if isinstance(last, dict) and number == 0:
                    continue
            if noraise and key not in last:
                break
            nodes.append(last[key])
            keys.append(key)
        return nodes, keys

    def get_raw_range(self, path):
        """Locate the position of a node in the YAML within the raw text

        See also `get_raw()` if you want to get the content of the unparsed
        meta.yaml at a specific key.

        Args:
          path: The "path" to the node. Use numbers for lists ('source/1/url')

        Returns:
          a tuple of first_row, first_column, last_row, last_column
        """
        if not path or not self.renderer == RendererType.RUAMEL:
            if self.meta_yaml:
                return 0, 0, len(self.meta_yaml), len(self.meta_yaml[-1])
            else:
                return 0, 0, 0, 0

        nodes, keys = self._walk(path)
        nodes.pop()  # pop parsed value

        # get the start row/col for the value
        if isinstance(keys[-1], int):
            start_row, start_col = nodes[-1].lc.key(keys[-1])
        else:
            start_row, start_col = nodes[-1].lc.value(keys[-1])

        # getting the end is more complicated, we need to move
        # up the tree to the next item in order until one is not the last
        # item in its collection
        while nodes:
            node = nodes.pop()
            key = keys.pop()
            if isinstance(key, int):
                if key + 1 < len(node):
                    end_row, end_col = node.lc.key(key + 1)
                    break
            else:
                node_keys = list(node.keys())
                if key != node_keys[-1]:
                    next_key = node_keys[node_keys.index(key) + 1]
                    end_row, end_col = node.lc.key(next_key)
                    break
        else:  # reached end of file
            end_row = len(self.meta_yaml) - 1
            end_col = len(self.meta_yaml[end_row])

        # now go backward
        return (start_row, start_col, end_row, end_col)

    def get_raw(self, path):
        """Extracts the unparsed text for a node in the meta.yaml

        This may contain separators and other characters from
        the yaml!

        Args:
          path: Slash-separated path to the node. Numbers can be used
                to access indices in lists. A number '0' is ignored if
                the node is a dict (so 'source/0/url' will work even if
                there is only one url).

        Returns:
          Extracted raw text
        """
        start_row, start_col, end_row, end_col = self.get_raw_range(path)
        if start_row == end_row:
            return self.meta_yaml[start_row][start_col:end_col]

        lines = []
        # first row
        lines.append(self.meta_yaml[start_row][start_col:])
        # middle rows if any
        for row in range(start_row + 1, end_row):
            lines.append(self.meta_yaml[row])
        lines.append(self.meta_yaml[end_row][:end_col])
        return "\n".join(lines).strip()

    def get(self, path: str, default: Any = KeyError) -> Any:
        """Get a value or section from the recipe

        >>> recipe.get('requirements/build')
        ['setuptools]
        >>> recipe.get('source/0/url')
        'https://somewhere'

        The **path** is a ``/`` separated list of dictionary keys to
        be walked in the recipe meta data. Numeric sections in the path
        access list elements. Using ``0`` in the path will get the first
        element in a list or the contents directly if there is no list.
        I.e., `source/0/url` will always get the first url, whether or
        not the source section is a list.

        Args:
          path: Path through YAML
          default: If not KeyError, this value will be returned
                   if the path does not exist in the recipe
        Raises:
          KeyError if no default given and the path does not exist.
        """
        try:
            nodes, keys = self._walk(path)
        except (KeyError, TypeError):
            if default is not KeyError:
                return default
            raise KeyError(f"No '{path}' in Recipe {self}") from None
        res = nodes[-1]
        if default is not KeyError and res is None:
            return default
        return res

    def contains(self, path: str, value: str, default: Any = KeyError) -> bool:
        """Check if a value (string or list) contains a string
        >>> recipe.contains('build/script', 'pip')
        True
        The **path** is a ``/`` separated list of dictionary keys to
        be walked in the recipe meta data. Numeric sections in the path
        access list elements. Using ``0`` in the path will get the first
        element in a list or the contents directly if there is no list.
        I.e., `source/0/url` will always get the first url, whether or
        not the source section is a list.
        Args:
            path: Path through YAML
            value: The string to match
            default: If not KeyError, this value will be returned
                    if the path does not exist in the recipe
        Returns:
            Value match (bool).
        Raises:
            KeyError if no default given and the path does not exist.
        """
        res = self.get(path, default)
        if isinstance(res, str):
            return value in res
        if isinstance(res, list):
            for r in res:
                if value in r:
                    return True
        return False

    def patch(self, operations, increment_build_number=False):
        """Patch the recipe given a set of operations.
        Args:
            operations: operations to apply
        Returns:
            True if recipe was patched. (bool).
        """
        if self.skip:
            logging.warning(f"Not patching skipped recipe {self.recipe_dir}")
            return False
        if self.renderer != RendererType.RUAMEL:
            self.renderer = RendererType.RUAMEL
            self.render()
        jsonschema.validate(operations, self.schema)
        for op in operations:
            for package in self.packages.values():
                self._patch(op, package)
                self.save()
                self.render()
        if self.is_modified():
            if increment_build_number:
                self._increment_build_number()
                self.save()
                self.render()
            logging.info(f"Patch applied: {self.recipe_dir}")
            return True
        return False

    def _patch(self, operation, package):
        # read operation parameters
        op = operation["op"]
        path = operation["path"].replace("@output/", package.path_prefix)
        match = operation.get("match", ".*")
        expanded_match = re.compile(
            f"\s+(?P<pattern>{match}[^#]*)(?P<selector>\s*#.*)?"
        )
        value = operation.get("value", [""])
        if value == []:
            value = [""]
        opop = deepcopy(operation)
        opop["path"] = path

        # infer data type
        in_list = False
        raw_value = self.get(path, "NOPE")
        if op == "remove":
            if raw_value == "NOPE":
                return
        elif op == "replace":
            if raw_value == "NOPE":
                return
            else:
                if isinstance(raw_value, str):
                    if re.search(match, raw_value):
                        parent_path, parent_name = path.rsplit("/", 1)
                        path = parent_path
                        value = [value]
                else:
                    in_list = True
        elif op == "add":
            parent_path, parent_name = path.rsplit("/", 1)
            if raw_value == "NOPE":
                # path not found - add section and return

                # We may be trying to add something that would be removed with
                # the current selector_dict. In that case, better leave it out.
                # Example: adding skip: True # [py<35]
                if isinstance(value, list):
                    rval = renderer._apply_selector(
                        "\n".join(value), self.selector_dict
                    )
                else:
                    rval = renderer._apply_selector(value, self.selector_dict)
                if rval.strip() == "":
                    logging.warning(f"Skipping op due to selector:{opop}")
                    return

                # finding range of direct parent
                # (not doing the leg work of going up the tree if parent is not found)
                try:
                    (start_row, start_col, end_row, _) = self.get_raw_range(parent_path)
                except KeyError:
                    logging.warning(f"Path not found while applying op:{opop}")
                else:
                    # adding value to end of parent
                    # if value is a list, adding as a list to parent
                    # if value is a string, adding as parent: value
                    parent_range = deepcopy(self.meta_yaml[start_row:end_row])
                    parent_insert_index = 0
                    for i, e in reversed(list(enumerate(parent_range))):
                        if e.strip():
                            parent_insert_index = i + 1
                            break
                    if isinstance(value, list):
                        parent_range.insert(
                            parent_insert_index, " " * start_col + f"{parent_name}:"
                        )
                        for val in value:
                            parent_range.insert(
                                parent_insert_index + 1, " " * start_col + f"  - {val}"
                            )
                    else:
                        parent_range.insert(
                            parent_insert_index,
                            " " * start_col + f"{parent_name}: {value}",
                        )
                    self.meta_yaml[start_row:end_row] = parent_range
                    return
            else:
                # path found - store value to add
                if isinstance(raw_value, str):
                    if re.search(match, raw_value):
                        path = parent_path
                        expanded_match = re.compile("NOPE")
                        if isinstance(value, list):
                            value = [parent_name + ": " + val for val in value]
                        else:
                            value = [f"{parent_name}: {value}"]
                else:
                    in_list = True

        # get initial section range
        try:
            (start_row, start_col, end_row, _) = self.get_raw_range(path)
        except KeyError:
            logging.warning(f"Path not found while applying op:{opop}")
            return
        range = deepcopy(self.meta_yaml[start_row:end_row])

        # find matching elements
        match_lines = {}
        for i, line in enumerate(range):
            if not line.lstrip().startswith("#"):
                m = expanded_match.search(line)
                if m:
                    match_lines[i] = m
        match_lines = dict(sorted(match_lines.items(), reverse=True))

        # remove elements and find insert position
        new_range = deepcopy(range)
        insert_index = 0
        index_set = False
        for i, m in match_lines.items():
            new_range.pop(i)
            insert_index = i
            index_set = True
        range = new_range
        if not index_set:
            for i, e in reversed(list(enumerate(range))):
                if e.strip():
                    insert_index = i + 1
                    break

        # add elements
        if op == "add" or (op == "replace" and match_lines):
            to_insert = set()
            for new_val in value:
                for i, m in match_lines.items():
                    to_insert.add(
                        m.string.replace(m.groupdict()["pattern"], new_val).replace(
                            "#", "  #", 1
                        )
                    )
            if not to_insert:
                to_insert = set(value)
            for new_val in to_insert:
                if in_list:
                    range.insert(
                        insert_index, " " * start_col + f"- {new_val.strip(' -')}"
                    )
                else:
                    range.insert(insert_index, " " * start_col + f"{new_val.strip()}")

        # apply change
        self.meta_yaml[start_row:end_row] = range

    def _increment_build_number(self):
        try:
            build_number = int(self.orig.meta["build"]["number"]) + 1
        except (KeyError, TypeError):
            logging.error(f"No build number found for {self.recipe_dir}")
            return
        patterns = (
            ("(?=\s*?)number:\s*([0-9]+)", "number: {}".format(build_number)),
            (
                '(?=\s*?){%\s*set build_number\s*=\s*"?([0-9]+)"?\s*%}',
                "{{% set build_number = {} %}}".format(build_number),
            ),
            (
                '(?=\s*?){%\s*set build\s*=\s*"?([0-9]+)"?\s*%}',
                "{{% set build = {} %}}".format(build_number),
            ),
        )
        text = "\n".join(self.meta_yaml)
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)
        self.meta_yaml = text.split("\n")


class Dep:
    """A dependency

    Args:
        raw_dep (str): A dependency string. E.g. "numpy <1.24"
        path (str): Path in the recipe. E.g. outputs/1/requirements/run

    Attributes:
        raw_dep (str): A dependency string. E.g. "numpy <1.24"
        pkg (str): The package part. E.g. "numpy"
        variable (str): The constraint part. E.g. "<1.24"
        path (str): Path in the recipe. E.g. outputs/1/requirements/run
    """

    def __init__(self, raw_dep: str, path: str):
        """A dependency

        Args:
            raw_dep (str): A dependency string. E.g. "numpy <1.24"
        """
        self.raw_dep = str(raw_dep)
        splits = re.split(r"[\s<=>]", self.raw_dep, 1)
        self.pkg = splits[0].strip()
        self.constraint = ""
        if len(splits) > 1:
            self.constraint = splits[1]
        self.path = path

    def __str__(self) -> str:
        return str(self.raw_dep)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} "{self.raw_dep}"'


@dataclass
class Package:
    """A rendered package."""

    recipe: Recipe = None
    name: str = None
    version: str = None
    number: str = None
    group: str = None
    build: Set[Dep] = field(default_factory=set)
    host: Set[Dep] = field(default_factory=set)
    run: Set[Dep] = field(default_factory=set)
    run_constrained: Set[Dep] = field(default_factory=set)
    run_exports: Set[str] = field(default_factory=set)
    ignore_run_exports: Set[str] = field(default_factory=set)
    test: Set[Dep] = field(default_factory=set)
    is_noarch: bool = False
    path_prefix: str = ""
    git_info: object = None

    def __getitem__(self, key: str) -> Any:
        """Access this dataclass attributes through square brackets.

        Args:
            key (str): An attribute name of this data class.

        Returns:
            Any: The value of the attribute.
        """
        return getattr(self, key)

    def get(self, key: str, default=None) -> Any:
        """Access this dataclass attributes through a getter.

        Args:
            key (str): An attribute name of this data class.
            default (_type_, optional): Default value. Defaults to None.

        Returns:
            Any: The value of the attribute.
        """
        try:
            return getattr(self, key, default)
        except KeyError:
            return default

    def has_dep(self, section: str, pkg_name: str) -> bool:
        """Returns true if the package is present in the given section.

        Args:
            section (str): A section. E.g. "build", "host", "run", "run_constrained
            pkg_name (str): A package name.

        Returns:
            bool: True if the package is present in the given section.
        """
        return any([pkg_name.lower() == dep.pkg.lower() for dep in self[section]])

    def merge_deps(self, other: "Package"):
        """Merge dependency list of another Package object into this Package.
        This is especially useful to create an aggregate of multiple variants.

        Args:
            other (Package): The other Package.
        """
        self.build.update(other.build)
        self.host.update(other.host)
        self.run.update(other.run)
        self.run_constrained.update(other.run_constrained)
        self.run_exports.update(other.run_exports)
        self.ignore_run_exports.update(other.ignore_run_exports)


def render(
    recipe_path: Path,
    subdir: List[str] = None,
    python: List[str] = None,
    others: Dict[str, Any] = None,
    return_exceptions: bool = False,
    renderer: RendererType = None,
) -> List[Recipe]:
    """Render a recipe

    Args:
        recipe_path (Path): Path to a recipe.
        subdir (List[str], optional): A list of subdir to render for. E.g. ["linux-64", "win-64"]. Defaults to None to render all subdirs.
        python (List[str], optional): A list of python version to render for. E.g. ["3.10", "3.11"]. Defaults to None to render all python.
        others (Dict[str,Any], optional): Additional variants configuration. E.g. {"blas_impl" : "openblas"} Defaults to None.
        return_exceptions (bool, optional): Whether to handle errors as exceptions. Defaults to False.
        renderer (RendererType, optional): Renderer backend. Defautls to PYYAML.

    Returns:
        List[Recipe]: A list of rendered Recipe, one per variant.
    """

    # gather all possible variants
    if others is None:
        others = {"r_implementation": "r-base", "rust_compiler": "rust"}
    if renderer != RendererType.CONDA:
        variants = read_conda_build_config(recipe_path, subdir, python, others)
    else:
        variants = []
        if not python:
            python = ["3.8", "3.9", "3.10", "3.11"]
        for s, p in list(itertools.product(subdir, python)):
            variant = {"subdir": s, "python": [p]}
            variant.update(others)
            variant_id = {"subdir": [s], "python": [p]}
            variants.append((variant_id, variant))

    # render for each variant and combine similar results
    render_results = []
    for variant_id, variant in variants:
        r = Recipe.from_file(
            recipe_path, variant_id, variant, return_exceptions, renderer
        )
        if match := next((x for x in render_results if r.meta == x.meta), None):
            for key, value in r.variant_id.items():
                match.variant_id.get(key, set()).update(value)
        else:
            render_results.append(r)
    return render_results


def dump_render_results(render_results: List[Recipe], out: TextIO = sys.stdout) -> None:
    """Dumps a list of rendered variants of a recipe.

    Args:
        render_results (List[Recipe]): List of rendered variants.
        out (TextIO, optional): Output stream. Defaults to sys.stdout.

    """
    dumper.dump_render_results(render_results, out)
