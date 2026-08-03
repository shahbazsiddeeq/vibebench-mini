from src.solution import unused_imports
import pytest
import textwrap


def test_all_used():
    source = "import os\nprint(os.getcwd())\n"
    assert unused_imports(source) == []


def test_import_as_alias_binds_alias():
    source = "import numpy as np\n"
    assert unused_imports(source) == ["np"]


def test_dotted_import_unused():
    source = "import os.path\n"
    assert unused_imports(source) == ["os"]


def test_star_import_not_reported():
    # 'from m import *' binds no inspectable name; it must never be reported
    # (and never as a bogus name like '*').
    source = "from os import *\n"
    assert unused_imports(source) == []


def test_name_only_inside_string_is_unused():
    # 're' appears only as text inside a string literal, which is not a use.
    source = 'import re\ns = "re.compile(x)"\n'
    assert unused_imports(source) == ["re"]


def test_real_use_beats_string_mention():
    source = 'import re\nnote = "use re here"\nre.compile("x")\n'
    assert unused_imports(source) == []
