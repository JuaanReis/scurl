try:
    from importlib.metadata import version
    __version__ = version("scurl")
except Exception:
    __version__ = "dev"