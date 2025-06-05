from pathlib import Path


class _Config:
    def __init__(self):
        self._root_dir: Path = Path("app")

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    @root_dir.setter
    def root_dir(self, value: str | Path) -> None:
        self._root_dir = Path(value)


config: _Config = _Config()
