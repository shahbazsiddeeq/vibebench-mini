from src.solution import unused_imports
import pytest
import textwrap


def test_basic():
    source = "import os\nimport sys\nprint(os.getcwd())\n"
    assert unused_imports(source) == ["sys"]


def test_all_used():
    source = "import os\nprint(os.getcwd())\n"
    assert unused_imports(source) == []


def test_from_import_alias():
    source = "from math import sqrt as s\nfrom math import pi\nprint(pi)\n"
    assert unused_imports(source) == ["s"]


def test_import_as_alias_binds_alias():
    source = "import numpy as np\n"
    assert unused_imports(source) == ["np"]


def test_dotted_import_binds_top_package():
    source = "import os.path\nprint(os.path.join('a', 'b'))\n"
    assert unused_imports(source) == []


def test_dotted_import_unused():
    source = "import os.path\n"
    assert unused_imports(source) == ["os"]


def test_source_order():
    source = textwrap.dedent(
        """
        import a
        import b
        import c
        print(b)
        """
    )
    assert unused_imports(source) == ["a", "c"]


def test_star_import_not_reported():
    # 'from m import *' binds no inspectable name; it must never be reported
    # (and never as a bogus name like '*').
    source = "from os import *\n"
    assert unused_imports(source) == []


def test_star_import_alongside_unused():
    source = "from os import *\nimport sys\n"
    assert unused_imports(source) == ["sys"]


def test_name_only_inside_string_is_unused():
    # 're' appears only as text inside a string literal, which is not a use.
    source = 'import re\ns = "re.compile(x)"\n'
    assert unused_imports(source) == ["re"]


def test_name_only_inside_comment_is_unused():
    source = "import json  # json is handy\n"
    assert unused_imports(source) == ["json"]


def test_real_use_beats_string_mention():
    source = 'import re\nnote = "use re here"\nre.compile("x")\n'
    assert unused_imports(source) == []


def test_syntax_error_raises():
    with pytest.raises(ValueError):
        unused_imports("import \n")
