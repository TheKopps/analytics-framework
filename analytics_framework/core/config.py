from pathlib import Path
from typing import Any

import yaml


class Config:
    """
    Centralized configuration object for analytics projects.
    """

    def __init__(self, data: dict[str, Any]):
        self.data = data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        return cls(data)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Config":
        path = Path(path)

        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return cls(data)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.

        Example:
        config.get("paths.raw_data")
        """
        keys = key.split(".")
        value = self.data

        for item in keys:
            if not isinstance(value, dict) or item not in value:
                return default
            value = value[item]

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.

        Example:
        config.set("paths.raw_data", "data/raw")
        """
        keys = key.split(".")
        data = self.data

        for item in keys[:-1]:
            data = data.setdefault(item, {})

        data[keys[-1]] = value

    def to_dict(self) -> dict[str, Any]:
        return self.data

    def resolve_path(self, key: str, base_path: str | Path | None = None) -> Path:
        """
        Resolve a path from the configuration.

        Example:
        config.resolve_path("paths.raw_data")
        """
        value = self.get(key)

        if value is None:
            raise KeyError(f"Configuration key not found: {key}")

        path = Path(value)

        if base_path is not None and not path.is_absolute():
            path = Path(base_path) / path

        return path
