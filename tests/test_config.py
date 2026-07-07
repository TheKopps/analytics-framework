from pathlib import Path

from analytics_framework import Config


def test_config_get_and_set_values():
    config = Config.from_dict(
        {
            "project": {
                "name": "Demo Project",
            },
            "paths": {
                "raw_data": "data/raw",
            },
        }
    )

    assert config.get("project.name") == "Demo Project"
    assert config.get("paths.raw_data") == "data/raw"
    assert config.get("missing.key", "default") == "default"

    config.set("pipeline.stop_on_error", False)

    assert config.get("pipeline.stop_on_error") is False


def test_config_resolve_path(tmp_path):
    config = Config.from_dict(
        {
            "paths": {
                "reports": "reports",
            }
        }
    )

    resolved_path = config.resolve_path(
        "paths.reports",
        base_path=tmp_path,
    )

    assert resolved_path == Path(tmp_path) / "reports"