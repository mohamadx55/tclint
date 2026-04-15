from pathlib import Path

from tclint.commands.plugins import PluginManager
from tclint.parser import Parser

MY_DIR = Path(__file__).parent.resolve()
TEST_DATA_DIR = MY_DIR / "data"


def test_load_openroad():
    plugins = PluginManager()
    loaded = plugins.load_from_spec(TEST_DATA_DIR / "openroad.json")
    assert isinstance(loaded, dict)


def test_load_invalid():
    plugins = PluginManager()
    loaded = plugins.load_from_spec(TEST_DATA_DIR / "invalid.json")
    assert loaded is None


def test_load_py():
    plugins = PluginManager(trust_uninstalled=True)
    loaded = plugins.load_from_py(TEST_DATA_DIR / "dynamic.py")
    assert isinstance(loaded, dict)

    plugins = PluginManager(trust_uninstalled=False)
    loaded = plugins.load_from_py(TEST_DATA_DIR / "dynamic.py")
    assert loaded is None


def test_load_py_invalid():
    plugins = PluginManager()
    loaded = plugins.load_from_py(TEST_DATA_DIR / "dynamic_invalid.py")
    assert loaded is None


def test_dynamic_int_plugin():
    plugins = PluginManager(trust_uninstalled=True)
    commands = plugins.get_commands([TEST_DATA_DIR / "dynamic_int.py"])

    parser = Parser(commands=commands)
    parser.parse("open_block blockname -check 2")
    assert len(parser.violations) == 0

    parser = Parser(commands=commands)
    parser.parse("open_block blockname -check test")
    assert len(parser.violations) > 0
    assert "invalid value for open_block -check: got test, expected int" in str(
        parser.violations[0]
    )

    parser = Parser(commands=commands)
    parser.parse("open_block blockname -check")
    assert len(parser.violations) > 0
    assert "expected int value after -check" in str(parser.violations[0])
