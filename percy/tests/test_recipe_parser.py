"""
File:           test_recipe_parser.py
Description:    Unit tests for the recipe parser class and tools
"""
# Allows older versions of python to use newer forms of type annotation. There
# are major features introduced in 3.9 and 3.10.
from __future__ import annotations

from pathlib import Path
from typing import Final

import pytest

from percy.render import recipe_parser

# Path to supplementary files used in test cases
TEST_FILES_PATH = "percy/tests/test_aux_files"

# Long multi-line description string found in the `simple-recipe.yaml` test file
SIMPLE_DESCRIPTION: Final[
    str
] = "This is a PEP '561 type stub package for the toml package.\nIt can be used by type-checking tools like mypy, pyright,\npytype, PyCharm, etc. to check code that uses toml."  # pylint: disable=line-too-long


def load_file(file: Path | str) -> str:
    """
    Loads a file into a single string
    :param file:    Filename of the file to read
    :return: Text from the file
    """
    with open(Path(file), "r", encoding="utf-8") as f:
        return f.read()


def load_recipe(file_name: str) -> recipe_parser.RecipeParser:
    """
    Convenience function that simplifies initializing a recipe parser.
    :param file_name:   File name of the test recipe to load
    :return: RecipeParser instance, based on the file
    """
    recipe = load_file(f"{TEST_FILES_PATH}/{file_name}")
    return recipe_parser.RecipeParser(recipe)


## Construction and rendering sanity checks ##


def test_construction() -> None:
    """
    Tests the construction of a recipe parser instance with a simple, common
    example file.
    """
    types_toml = load_file(f"{TEST_FILES_PATH}/types-toml.yaml")
    parser = recipe_parser.RecipeParser(types_toml)
    assert parser._init_content == types_toml  # pylint: disable=protected-access
    assert parser._vars_tbl == {  # pylint: disable=protected-access
        "name": "types-toml",
        "version": "0.10.8.6",
    }
    assert not parser._is_modified  # pylint: disable=protected-access
    # TODO assert on tree structure
    # TODO assert on selectors table
    # assert parser._root == TODO


def test_str() -> None:
    """
    Tests string casting
    """
    parser = load_recipe("simple-recipe.yaml")
    assert str(parser) == load_file(f"{TEST_FILES_PATH}/simple-recipe_to_str.out")
    # Regression test: Run a function a second time to ensure that `SelectorInfo::__str__()` doesn't accidentally purge
    # the underlying stack when the string is being rendered.
    assert str(parser) == load_file(f"{TEST_FILES_PATH}/simple-recipe_to_str.out")
    assert not parser.is_modified()


def test_eq() -> None:
    """
    Tests equivalency function
    """
    parser0 = load_recipe("simple-recipe.yaml")
    parser1 = load_recipe("simple-recipe.yaml")
    parser2 = load_recipe("types-toml.yaml")
    assert parser0 == parser1
    assert parser0 != parser2
    assert not parser0.is_modified()
    assert not parser1.is_modified()
    assert not parser2.is_modified()


def test_dog_food_easy() -> None:
    """
    Test "eating our own dog food": Take a recipe, construct a parser, re-render
    and ensure the output matches the input.

    This is the "easy" recipe test, to ensure compatibility with "basic" recipe
    structures with no gotchas.
    """
    types_toml = load_file(f"{TEST_FILES_PATH}/types-toml.yaml")
    parser = recipe_parser.RecipeParser(types_toml)
    assert parser.render() == types_toml


def test_dog_food_medium() -> None:
    """
    Test "eating our own dog food": Take a recipe, construct a parser, re-render
    and ensure the output matches the input.

    This is the "medium" recipe test, to ensure compatibility with some more
    contrived examples
    """
    simple = load_file(f"{TEST_FILES_PATH}/simple-recipe.yaml")
    parser = recipe_parser.RecipeParser(simple)
    assert parser.render() == simple


@pytest.mark.skip(reason="To be re-enable when PKG-2964 is fixed")
def test_loading_obj_in_list() -> None:
    """
    Regression test: at one point, the parser would crash loading this file,
    containing an object in a list.
    """
    replace = load_file(f"{TEST_FILES_PATH}/simple-recipe_test_patch_replace.yaml")
    parser = recipe_parser.RecipeParser(replace)
    assert parser.render() == replace


def test_dog_food_multi_output() -> None:
    """
    Test "eating our own dog food": Take a recipe, construct a parser, re-render
    and ensure the output matches the input.

    This tests multi-output recipes, to ensure compatibility with some more
    complex recipe examples.
    """
    multi = load_file(f"{TEST_FILES_PATH}/multi-output.yaml")
    parser = recipe_parser.RecipeParser(multi)
    assert parser.render() == multi


def test_render_to_object() -> None:
    """
    Tests rendering a recipe to an object format.
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.render_to_object() == {
        "about": {
            "description": SIMPLE_DESCRIPTION,
            "license": "Apache-2.0 AND MIT",
            "summary": "This is a small recipe for testing",
        },
        "test_var_usage": {
            "foo": "{{ version }}",
            "bar": [
                "baz",
                "{{ zz_non_alpha_first }}",
                "blah",
                "This {{ name }} is silly",
                "last",
            ],
        },
        "build": {"is_true": True, "skip": True, "number": 0},
        "package": {"name": "{{ name|lower }}"},
        "requirements": {
            "empty_field1": None,
            "host": ["setuptools", "fakereq"],
            "empty_field2": None,
            "run": ["python"],
            "empty_field3": None,
        },
        "multi_level": {
            "list_3": ["ls", "sl", "cowsay"],
            "list_2": ["cat", "bat", "mat"],
            "list_1": ["foo", "bar"],
        },
    }


## Values ##


def test_list_value_paths() -> None:
    """
    Tests retrieval of all value paths
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.list_value_paths() == [
        "/package/name",
        "/build/number",
        "/build/skip",
        "/build/is_true",
        "/requirements/empty_field1",
        "/requirements/host/0",
        "/requirements/host/1",
        "/requirements/empty_field2",
        "/requirements/run/0",
        "/requirements/empty_field3",
        "/about/summary",
        "/about/description",
        "/about/license",
        "/multi_level/list_1/0",
        "/multi_level/list_1/1",
        "/multi_level/list_2/0",
        "/multi_level/list_2/1",
        "/multi_level/list_2/2",
        "/multi_level/list_3/0",
        "/multi_level/list_3/1",
        "/multi_level/list_3/2",
        "/test_var_usage/foo",
        "/test_var_usage/bar/0",
        "/test_var_usage/bar/1",
        "/test_var_usage/bar/2",
        "/test_var_usage/bar/3",
        "/test_var_usage/bar/4",
    ]


def test_contains_value() -> None:
    """
    Tests retrieval of a value from a parsed YAML example.
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.contains_value("/build/number")
    assert parser.contains_value("/build/number/")
    assert parser.contains_value("/build")
    assert parser.contains_value("/requirements/host/0")
    assert parser.contains_value("/requirements/host/1")
    # Comments in lists could throw-off array indexing
    assert parser.contains_value("/multi_level/list_1/1")
    # Path not found cases
    assert not parser.contains_value("/invalid/fake/path")
    assert not parser.is_modified()


def test_get_value() -> None:
    """
    Tests retrieval of a value from a parsed YAML example.
    """
    parser = load_recipe("simple-recipe.yaml")
    # Return a single value
    assert parser.get_value("/build/number") == 0
    assert parser.get_value("/build/number/") == 0
    # Return a compound value
    assert parser.get_value("/build") == {
        "number": 0,
        "skip": True,
        "is_true": True,
    }
    assert parser.get_value("/build/") == {
        "number": 0,
        "skip": True,
        "is_true": True,
    }
    # Return a Jinja value (substitution flag not in use)
    assert parser.get_value("/package/name") == "{{ name|lower }}"
    # Return a value in a list
    assert parser.get_value("/requirements/host") == ["setuptools", "fakereq"]
    assert parser.get_value("/requirements/host/") == ["setuptools", "fakereq"]
    assert parser.get_value("/requirements/host/0") == "setuptools"
    assert parser.get_value("/requirements/host/1") == "fakereq"
    # Return a multiline string
    assert parser.get_value("/about/description") == SIMPLE_DESCRIPTION
    assert parser.get_value("/about/description/") == SIMPLE_DESCRIPTION
    # Path not found cases
    with pytest.raises(KeyError):
        parser.get_value("/invalid/fake/path")
    assert parser.get_value("/invalid/fake/path", 42) == 42
    # Tests that a user can pass `None` without throwing
    assert parser.get_value("/invalid/fake/path", None) is None
    # Comments in lists could throw-off array indexing
    assert parser.get_value("/multi_level/list_1/1") == "bar"
    # Render a recursive, complex type.
    assert parser.get_value("/test_var_usage", sub_vars=True) == {
        "foo": "0.10.8.6",
        "bar": [
            "baz",
            42,
            "blah",
            "This types-toml is silly",
            "last",
        ],
    }
    assert not parser.is_modified()


def test_get_value_with_var_subs() -> None:
    """
    Tests retrieval of a value from a parsed YAML example, with Jinja variable substitutions enabled.
    """
    parser = load_recipe("simple-recipe.yaml")
    # TODO re-enable checks
    # No change on lines without any variable substitutions
    # assert parser.get_value("/requirements/host", sub_vars=True) == ["setuptools", "fakereq"]

    ## Test base types
    assert parser.get_value("/test_var_usage/foo", sub_vars=True) == "0.10.8.6"
    assert parser.get_value("/test_var_usage/bar/1", sub_vars=True) == 42
    # Test string with `|lower` function applied
    assert parser.get_value("/package/name", sub_vars=True) == "types-toml"
    # Test collection types
    assert parser.get_value("/test_var_usage/bar", sub_vars=True) == [
        "baz",
        42,
        "blah",
        "This types-toml is silly",
        "last",
    ]
    assert parser.get_value("/test_var_usage", sub_vars=True) == {
        "foo": "0.10.8.6",
        "bar": [
            "baz",
            42,
            "blah",
            "This types-toml is silly",
            "last",
        ],
    }
    assert not parser.is_modified()


def test_find_value() -> None:
    """
    Tests finding a value from a parsed YAML example.
    """
    parser = load_recipe("simple-recipe.yaml")
    # Values in the recipe
    assert parser.find_value(None) == [
        "/requirements/empty_field1",
        "/requirements/empty_field2",
        "/requirements/empty_field3",
    ]
    assert parser.find_value("fakereq") == ["/requirements/host/1"]
    assert parser.find_value(True) == ["/build/skip", "/build/is_true"]
    assert parser.find_value("foo") == ["/multi_level/list_1/0"]
    assert parser.find_value("Apache-2.0 AND MIT") == ["/about/license"]
    # Values not in the recipe
    assert not parser.find_value(43)
    assert not parser.find_value("fooz")
    assert not parser.find_value("")
    # Values that are not supported for searching
    with pytest.raises(ValueError):
        parser.find_value(["foo", "bar"])
    with pytest.raises(ValueError):
        parser.find_value(("foo", "bar"))
    with pytest.raises(ValueError):
        parser.find_value({"foo": "bar"})
    # Find does not modify the parser
    assert not parser.is_modified()


## Variables ##


def test_list_variable() -> None:
    """
    Validates the list of variables found
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.list_variables() == ["zz_non_alpha_first", "name", "version"]
    assert not parser.is_modified()


def test_contains_variable() -> None:
    """
    Validates checking if a variable exists in a recipe
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.contains_variable("zz_non_alpha_first")
    assert parser.contains_variable("name")
    assert parser.contains_variable("version")
    assert not parser.contains_variable("fake_var")
    assert not parser.is_modified()


def test_get_variable() -> None:
    """
    Tests the value returned from fetching a variable
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.get_variable("zz_non_alpha_first") == 42
    assert parser.get_variable("name") == "types-toml"
    assert parser.get_variable("version") == "0.10.8.6"
    with pytest.raises(KeyError):
        parser.get_variable("fake_var")
    assert parser.get_variable("fake_var", 43) == 43
    # Tests that a user can pass `None` without throwing
    assert parser.get_variable("fake_var", None) is None
    assert not parser.is_modified()


def test_set_variable() -> None:
    """
    Tests setting and adding a variable
    """
    parser = load_recipe("simple-recipe.yaml")
    parser.set_variable("name", "foobar")
    parser.set_variable("zz_non_alpha_first", 24)
    # Ensure a missing variable gets added
    parser.set_variable("DNE", "The limit doesn't exist")
    # Validate
    assert parser.is_modified()
    assert parser.list_variables() == [
        "zz_non_alpha_first",
        "name",
        "version",
        "DNE",
    ]
    assert parser.get_variable("name") == "foobar"
    assert parser.get_variable("zz_non_alpha_first") == 24
    assert parser.get_variable("DNE") == "The limit doesn't exist"


def test_del_variable() -> None:
    """
    Tests deleting a variable
    """
    parser = load_recipe("simple-recipe.yaml")
    parser.del_variable("name")
    # Ensure a missing var doesn't crash a delete
    parser.del_variable("DNE")
    # Validate
    assert parser.is_modified()
    assert parser.list_variables() == ["zz_non_alpha_first", "version"]
    with pytest.raises(KeyError):
        parser.get_variable("name")


def test_get_variable_references() -> None:
    """
    Tests generating a list of paths that use a variable
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.get_variable_references("version") == [
        "/test_var_usage/foo",
    ]
    assert parser.get_variable_references("zz_non_alpha_first") == [
        "/test_var_usage/bar/1",
    ]
    assert parser.get_variable_references("name") == [
        "/package/name",
        "/test_var_usage/bar/3",
    ]
    assert not parser.is_modified()


## Selectors ##


def test_list_selectors() -> None:
    """
    Validates the list of selectors found
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.list_selectors() == ["[unix]", "[py<37]", "[unix and win]"]
    assert not parser.is_modified()


def test_contains_selectors() -> None:
    """
    Validates checking if a selector exists in a recipe
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.contains_selector("[py<37]")
    assert parser.contains_selector("[unix]")
    assert not parser.contains_selector("[fake selector]")
    assert not parser.is_modified()


def test_get_selector_paths() -> None:
    """
    Tests the paths returned from fetching a selector
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.get_selector_paths("[py<37]") == ["/build/skip"]
    assert parser.get_selector_paths("[unix]") == [
        "/package/name",
        "/requirements/host/0",
        "/requirements/host/1",
    ]
    assert not parser.get_selector_paths("[fake selector]")
    assert not parser.is_modified()


def test_add_selector() -> None:
    """
    Tests adding a selector to a recipe
    """
    parser = load_recipe("simple-recipe.yaml")
    # Test that selector validation is working
    with pytest.raises(KeyError):
        parser.add_selector("/package/path/to/fake/value", "[unix]")
    with pytest.raises(ValueError):
        parser.add_selector("/build/number", "bad selector")
    assert not parser.is_modified()

    # Add selectors to lines without existing selectors
    parser.add_selector("/requirements/empty_field3", "[unix]")
    parser.add_selector("/multi_level/list_1/0", "[unix]")
    parser.add_selector("/build/number", "[win]")
    parser.add_selector("/multi_level/list_2/1", "[win]")
    assert parser.get_selector_paths("[unix]") == [
        "/package/name",
        "/requirements/host/0",
        "/requirements/host/1",
        "/requirements/empty_field3",
        "/multi_level/list_1/0",
    ]
    assert parser.get_selector_paths("[win]") == [
        "/build/number",
        "/multi_level/list_2/1",
    ]

    # Add selectors to existing selectors
    parser.add_selector("/requirements/host/0", "[win]", recipe_parser.SelectorConflictMode.REPLACE)
    assert parser.get_selector_paths("[win]") == [
        "/build/number",
        "/requirements/host/0",
        "/multi_level/list_2/1",
    ]
    parser.add_selector("/requirements/host/1", "[win]", recipe_parser.SelectorConflictMode.AND)
    assert parser.get_selector_paths("[unix and win]") == ["/requirements/host/1", "/requirements/empty_field2"]
    parser.add_selector("/build/skip", "[win]", recipe_parser.SelectorConflictMode.OR)
    assert parser.get_selector_paths("[py<37 or win]") == ["/build/skip"]
    parser.add_selector("/requirements/run/0", "[win]", recipe_parser.SelectorConflictMode.AND)
    assert parser.get_selector_paths("[win]") == [
        "/build/number",
        "/requirements/host/0",
        "/requirements/run/0",
        "/multi_level/list_2/1",
    ]

    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_add_selector.yaml")
    assert parser.is_modified()


def test_remove_selector() -> None:
    """
    Tests removing a selector to a recipe
    """
    parser = load_recipe("simple-recipe.yaml")
    # Test that selector validation is working
    with pytest.raises(KeyError):
        parser.remove_selector("/package/path/to/fake/value")

    # Don't fail when a selector doesn't exist on a line
    assert parser.remove_selector("/build/number") is None
    # Don't remove a non-selector comment
    assert parser.remove_selector("/requirements/run/0") is None
    assert not parser.is_modified()

    # Remove a selector
    assert parser.remove_selector("/package/name") == "[unix]"
    assert parser.get_selector_paths("[unix]") == [
        "/requirements/host/0",
        "/requirements/host/1",
    ]
    # Remove a selector with a comment
    assert parser.remove_selector("/requirements/host/1") == "[unix]"
    assert parser.get_selector_paths("[unix]") == [
        "/requirements/host/0",
    ]
    # Remove a selector with a "double comment (extra `#` symbols used)"
    assert parser.remove_selector("/requirements/empty_field2") == "[unix and win]"
    assert not parser.get_selector_paths("[unix and win]")

    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_remove_selector.yaml")
    assert parser.is_modified()


## Patch and Search ##


def test_patch_schema_validation() -> None:
    """
    Tests edge cases that should trigger an exception on JSON patch schema
    validation. Valid schemas are inherently tested in the other patching tests.
    """
    parser = load_recipe("simple-recipe.yaml")
    # Invalid enum/unknown op
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "fakeop",
                "path": "/build/number",
                "value": 42,
            }
        )
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "",
                "path": "/build/number",
                "value": 42,
            }
        )
    # Patch has extra field(s)
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "replace",
                "path": "/build/number",
                "value": 42,
                "extra": "field",
            }
        )
    # Patch is missing required fields
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "path": "/build/number",
                "value": 42,
            }
        )
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "replace",
                "value": 42,
            }
        )
    # Patch is missing required fields, based on `op`
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "add",
                "path": "/build/number",
            }
        )
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "replace",
                "path": "/build/number",
            }
        )
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "move",
                "path": "/build/number",
            }
        )
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "copy",
                "path": "/build/number",
            }
        )
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch(
            {
                "op": "test",
                "path": "/build/number",
            }
        )
    # Patch has invalid types in critical fields
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch({"op": "move", "path": 42, "value": 42})
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        parser.patch({"op": "move", "path": "/build/number", "from": 42})


def test_patch_path_invalid() -> None:
    """
    Tests if `patch` returns false on all ops when the path is not found.
    Also checks if the tree has been modified.
    """
    parser = load_recipe("simple-recipe.yaml")

    # Passing an empty path fails at the JSON schema validation layer, so it
    # applies to all patch functions.
    with pytest.raises(recipe_parser.JsonPatchValidationException):
        assert not (
            parser.patch(
                {
                    "op": "test",
                    "path": "",
                    "value": 42,
                }
            )
        )

    # add
    assert not (
        parser.patch(
            {
                "op": "add",
                "path": "/package/path/to/fake/value",
                "value": 42,
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "add",
                "path": "/build/number/0",
                "value": 42,
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "add",
                "path": "/multi_level/list2/4",
                "value": 42,
            }
        )
    )
    # remove
    assert not (
        parser.patch(
            {
                "op": "remove",
                "path": "/package/path/to/fake/value",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "remove",
                "path": "/build/number/0",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "remove",
                "path": "/multi_level/list2/4",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "remove",
                "path": "/build/skip/true",
            }
        )
    )
    # replace
    assert not (
        parser.patch(
            {
                "op": "replace",
                "path": "/build/number/0",
                "value": 42,
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "replace",
                "path": "/multi_level/list2/4",
                "value": 42,
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "replace",
                "path": "/build/skip/true",
                "value": 42,
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "replace",
                "path": "/package/path/to/fake/value",
                "value": 42,
            }
        )
    )

    # move, `path` is invalid
    assert not (
        parser.patch(
            {
                "op": "move",
                "path": "/package/path/to/fake/value",
                "from": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "move",
                "path": "/build/number/0",
                "from": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "move",
                "path": "/multi_level/list2/4",
                "from": "/about/summary",
            }
        )
    )
    # move, `from` is invalid
    assert not (
        parser.patch(
            {
                "op": "move",
                "from": "/package/path/to/fake/value",
                "path": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "move",
                "from": "/build/number/0",
                "path": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "move",
                "from": "/multi_level/list2/4",
                "path": "/about/summary",
            }
        )
    )

    # copy, `path` is invalid
    assert not (
        parser.patch(
            {
                "op": "copy",
                "path": "/package/path/to/fake/value",
                "from": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "copy",
                "path": "/build/number/0",
                "from": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "copy",
                "path": "/multi_level/list2/4",
                "from": "/about/summary",
            }
        )
    )
    # copy, `from` is invalid
    assert not (
        parser.patch(
            {
                "op": "copy",
                "from": "/package/path/to/fake/value",
                "path": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "copy",
                "from": "/build/number/0",
                "path": "/about/summary",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "copy",
                "from": "/multi_level/list2/4",
                "path": "/about/summary",
            }
        )
    )

    # test
    assert not (
        parser.patch(
            {
                "op": "test",
                "path": "/package/path/to/fake/value",
                "value": 42,
            }
        )
    )

    assert not parser.is_modified()


def test_patch_test() -> None:
    """
    Tests the `test` patch op. The `test` op may be useful for other test
    assertions, so it is tested before the other patch operations.
    """
    parser = load_recipe("simple-recipe.yaml")

    # Test that values match, as expected
    assert parser.patch(
        {
            "op": "test",
            "path": "/build/number",
            "value": 0,
        }
    )
    assert parser.patch(
        {
            "op": "test",
            "path": "/build",
            "value": {
                "number": 0,
                "skip": True,
                "is_true": True,
            },
        }
    )
    assert parser.patch(
        {
            "op": "test",
            "path": "/requirements/host",
            "value": ["setuptools", "fakereq"],
        }
    )
    assert parser.patch(
        {
            "op": "test",
            "path": "/requirements/host/1",
            "value": "fakereq",
        }
    )
    assert parser.patch(
        {
            "op": "test",
            "path": "/about/description",
            "value": SIMPLE_DESCRIPTION,
        }
    )
    # Test that values do not match, as expected
    assert not (
        parser.patch(
            {
                "op": "test",
                "path": "/build/number",
                "value": 42,
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "test",
                "path": "/build",
                "value": {
                    "number": 42,
                    "skip": True,
                },
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "test",
                "path": "/requirements/host",
                "value": ["not_setuptools", "fakereq"],
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "test",
                "path": "/requirements/host/1",
                "value": "other_fake",
            }
        )
    )
    assert not (
        parser.patch(
            {
                "op": "test",
                "path": "/about/description",
                "value": "other_fake\nmultiline",
            }
        )
    )

    # Ensure that `test` does not modify the tree
    assert not parser.is_modified()


def test_patch_add() -> None:
    """
    Tests the `add` patch op.
    """
    parser = load_recipe("simple-recipe.yaml")

    # As per the RFC, `add` will not construct multiple-levels of non-existing
    # structures. The containing object(s)/list(s) must exist.
    assert not parser.patch(
        {
            "op": "add",
            "path": "/build/fake/meaning_of_life",
            "value": 42,
        }
    )
    # Similarly, appending to a list
    assert not parser.patch(
        {
            "op": "add",
            "path": "/requirements/empty_field1/-/blah",
            "value": 42,
        }
    )
    assert not parser.is_modified()

    # Add primitive values
    assert parser.patch(
        {
            "op": "add",
            "path": "/build/meaning_of_life",
            "value": 42,
        }
    )
    assert parser.patch(
        {
            "op": "add",
            "path": "/package/is_cool_name",
            "value": True,
        }
    )

    # Add to empty-key node
    assert parser.patch(
        {
            "op": "add",
            "path": "/requirements/empty_field2",
            "value": "Not so empty now",
        }
    )

    # Add list items
    assert parser.patch(
        {
            "op": "add",
            "path": "/multi_level/list_2/1",
            "value": "We got it all on UHF",
        }
    )
    assert parser.patch(
        {
            "op": "add",
            "path": "/multi_level/list_1/0",
            "value": "There's just one place to go for all your spatula needs!",
        }
    )
    assert parser.patch(
        {
            "op": "add",
            "path": "/multi_level/list_1/-",
            "value": "Spatula City!",
        }
    )

    # Add a complex value
    assert parser.patch(
        {
            "op": "add",
            "path": "/test_var_usage/Stanley",
            "value": [
                "Oh, Joel Miller, you've just found the marble in the oatmeal.",
                "You're a lucky, lucky, lucky little boy.",
                "'Cause you know why?",
                "You get to drink from... the FIRE HOOOOOSE!",
            ],
        }
    )

    # Add a top-level complex value
    assert parser.patch(
        {
            "op": "add",
            "path": "/U62",
            "value": {
                "George": ["How'd you like your own TV show?", "You're on"],
                "Stanley": ["Ok"],
            },
        }
    )

    # Edge case: adding a value to an existing key (non-list) actually replaces
    # the value at that key, as per the RFC.
    assert parser.patch({"op": "add", "path": "/about/summary", "value": 62})

    # Sanity check: validate all modifications
    assert parser.is_modified()
    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_patch_add.yaml")


def test_patch_remove() -> None:
    """
    Tests the `remove` patch op.
    """
    parser = load_recipe("simple-recipe.yaml")

    # Remove primitive values
    assert parser.patch(
        {
            "op": "remove",
            "path": "/build/number",
        }
    )
    assert parser.patch(
        {
            "op": "remove",
            "path": "/package/name",
        }
    )

    # Remove empty-key node
    assert parser.patch(
        {
            "op": "remove",
            "path": "/requirements/empty_field2",
        }
    )

    # Remove list items
    assert parser.patch(
        {
            "op": "remove",
            "path": "/multi_level/list_2/0",
        }
    )
    # Ensure comments don't get erased
    assert parser.patch(
        {
            "op": "remove",
            "path": "/multi_level/list_1/1",
        }
    )

    # Remove a complex value
    assert parser.patch(
        {
            "op": "remove",
            "path": "/multi_level/list_3",
        }
    )

    # Remove a top-level complex value
    assert parser.patch(
        {
            "op": "remove",
            "path": "/about",
        }
    )

    # Sanity check: validate all modifications
    assert parser.is_modified()
    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_patch_remove.yaml")


def test_patch_replace() -> None:
    """
    Tests the `replace` patch op.
    """
    parser = load_recipe("simple-recipe.yaml")
    # Patch an integer
    assert parser.patch(
        {
            "op": "replace",
            "path": "/build/number",
            "value": 42,
        }
    )
    # Patch a bool
    assert parser.patch(
        {
            "op": "replace",
            "path": "/build/is_true",
            "value": False,
        }
    )
    # Patch a string
    assert parser.patch(
        {
            "op": "replace",
            "path": "/about/license",
            "value": "MIT",
        }
    )
    # Patch an array element
    assert parser.patch(
        {
            "op": "replace",
            "path": "/requirements/run/0",
            "value": "cpython",
        }
    )
    # Patch an element to become an array
    assert parser.patch(
        {
            "op": "replace",
            "path": "/about/summary",
            "value": [
                "The Trial",
                "Never Ends",
                "Picard",
            ],
        }
    )
    # Patch a multiline string
    assert parser.patch(
        {
            "op": "replace",
            "path": "/about/description",
            "value": ("This is a PEP 561\ntype stub package\nfor the toml package."),
        }
    )

    # Hard mode: replace a string with an object containing multiple types in
    # a complex data structure.
    assert parser.patch(
        {
            "op": "replace",
            "path": "/multi_level/list_2/1",
            "value": {"build": {"number": 42, "skip": True}},
        }
    )

    # Sanity check: validate all modifications
    assert parser.is_modified()
    # NOTE: That patches, as of writing, cannot preserve selectors
    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_patch_replace.yaml")


def test_patch_move() -> None:
    """
    Tests the `move` patch op.
    """
    parser = load_recipe("simple-recipe.yaml")
    # No-op moves should not corrupt our modification state.
    assert parser.patch(
        {
            "op": "move",
            "path": "/build/number",
            "from": "/build/number",
        }
    )
    # Special failure case: trying to "add" to an illegal path while the
    # "remove" path is still valid
    assert not parser.patch(
        {
            "op": "move",
            "path": "/build/number/0",
            "from": "/build/number",
        }
    )
    assert not parser.is_modified()
    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe.yaml")

    # Simple move
    assert parser.patch(
        {
            "op": "move",
            "path": "/requirements/number",
            "from": "/build/number",
        }
    )

    # Moving list item to a new key (replaces existing value)
    assert parser.patch(
        {
            "op": "move",
            "path": "/build/is_true",
            "from": "/multi_level/list_3/0",
        }
    )

    # Moving list item to a different list
    assert parser.patch(
        {
            "op": "move",
            "path": "/requirements/host/-",
            "from": "/multi_level/list_1/1",
        }
    )

    # Moving a list entry to another list entry position
    assert parser.patch(
        {
            "op": "move",
            "path": "/multi_level/list_2/0",
            "from": "/multi_level/list_2/1",
        }
    )

    # Moving a compound type
    assert parser.patch(
        {
            "op": "move",
            "path": "/multi_level/bar",
            "from": "/test_var_usage/bar",
        }
    )

    # Sanity check: validate all modifications
    assert parser.is_modified()
    # NOTE: That patches, as of writing, cannot preserve selectors
    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_patch_move.yaml")


def test_patch_copy() -> None:
    """
    Tests the `copy` patch op.
    """
    parser = load_recipe("simple-recipe.yaml")

    # Simple copy
    assert parser.patch(
        {
            "op": "copy",
            "path": "/requirements/number",
            "from": "/build/number",
        }
    )

    # Copying list item to a new key
    assert parser.patch(
        {
            "op": "copy",
            "path": "/build/is_true",
            "from": "/multi_level/list_3/0",
        }
    )

    # Copying list item to a different list
    assert parser.patch(
        {
            "op": "copy",
            "path": "/requirements/host/-",
            "from": "/multi_level/list_1/1",
        }
    )

    # Copying a list entry to another list entry position
    assert parser.patch(
        {
            "op": "copy",
            "path": "/multi_level/list_2/0",
            "from": "/multi_level/list_2/1",
        }
    )

    # Copying a compound type
    assert parser.patch(
        {
            "op": "copy",
            "path": "/multi_level/bar",
            "from": "/test_var_usage/bar",
        }
    )

    # Sanity check: validate all modifications
    assert parser.is_modified()
    # NOTE: That patches, as of writing, cannot preserve selectors
    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_patch_copy.yaml")


def test_search() -> None:
    """
    Tests searching for values
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.search(r"fake") == ["/requirements/host/1"]
    assert parser.search(r"^0$") == ["/build/number"]
    assert parser.search(r"true") == ["/build/skip", "/build/is_true"]
    assert parser.search(r"py.*") == ["/requirements/run/0", "/about/description"]
    assert parser.search(r"py.*", True) == ["/build/skip", "/requirements/run/0", "/about/description"]
    assert not parser.is_modified()


def test_search_and_patch() -> None:
    """
    Tests searching for values and then patching them
    """
    parser = load_recipe("simple-recipe.yaml")
    assert parser.search_and_patch(r"py.*", {"op": "replace", "value": "conda"}, True)
    assert parser.render() == load_file(f"{TEST_FILES_PATH}/simple-recipe_test_search_and_patch.yaml")
    assert parser.is_modified()


def test_diff() -> None:
    """
    Tests diffing output function
    """
    parser = load_recipe("simple-recipe.yaml")
    # Ensure a lack of a diff works
    assert parser.diff() == ""

    assert parser.patch(
        {
            "op": "replace",
            "path": "/build/number",
            "value": 42,
        }
    )
    # Patch a bool
    assert parser.patch(
        {
            "op": "replace",
            "path": "/build/is_true",
            "value": False,
        }
    )
    # Patch a string
    assert parser.patch(
        {
            "op": "replace",
            "path": "/about/license",
            "value": "MIT",
        }
    )
    assert parser.diff() == (
        "--- original\n"
        "\n"
        "+++ current\n"
        "\n"
        "@@ -6,9 +6,9 @@\n"
        "\n"
        "   name: {{ name|lower }}  # [unix]\n"
        " \n"
        " build:\n"
        "-  number: 0\n"
        "+  number: 42\n"
        "   skip: true  # [py<37]\n"
        "-  is_true: true\n"
        "+  is_true: false\n"
        " \n"
        " # Comment above a top-level structure\n"
        " requirements:\n"
        "@@ -27,7 +27,7 @@\n"
        "\n"
        "     This is a PEP '561 type stub package for the toml package.\n"
        "     It can be used by type-checking tools like mypy, pyright,\n"
        "     pytype, PyCharm, etc. to check code that uses toml.\n"
        "-  license: Apache-2.0 AND MIT\n"
        "+  license: MIT\n"
        " \n"
        " multi_level:\n"
        "   list_1:"
    )
