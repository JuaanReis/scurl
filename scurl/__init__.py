try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version("scurl")
except PackageNotFoundError:
    __version__ = "0.0.0"

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  

from pathlib import Path

_CONFIG_PATH = Path(__file__).parent.parent / "config.toml"

with _CONFIG_PATH.open("rb") as f:
    config = tomllib.load(f)