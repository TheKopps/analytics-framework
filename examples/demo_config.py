from pathlib import Path

from analytics_framework import Config

config = Config.from_yaml("examples/config_examples.yaml")

print("Project name:", config.get("project.name"))
print("Raw data path:", config.get("paths.raw_data"))
print("Logging enabled:", config.get("pipeline.enable_logging"))

reports_path = config.resolve_path("paths.reports", base_path=Path.cwd())

print("Resolved reports path:", reports_path)
