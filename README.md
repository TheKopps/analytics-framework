# Analytics Framework

[![CI](https://github.com/TheKopps/analytics-framework/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/TheKopps/analytics-framework/actions/workflows/ci.yml)

A reusable Python framework for business analytics, data quality, reporting and visualization.

## Overview

Analytics Framework is a lightweight Python package designed to help structure data analytics projects in a professional and reusable way.

The goal is to provide a common foundation for multiple analytics projects, including:

- Supply Chain Analytics
- Formula 1 Race Analytics
- Predictive Maintenance
- Job Market Intelligence

Instead of writing isolated scripts or notebooks, this framework provides reusable components for:

- pipeline orchestration
- configuration management
- logging
- error handling
- testing
- reporting
- visualization
- exports

## Key Features

- Modular pipeline engine
- Reusable `PipelineStep` abstraction
- Shared pipeline context
- YAML-based configuration system
- Centralized logging
- Custom error handling
- Execution timing for pipeline steps
- Unit tests with pytest
- Code quality checks with Ruff
- Continuous Integration with GitHub Actions

## Project Structure

```text
analytics-framework/
│
├── analytics_framework/
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logger.py
│   │   ├── pipeline.py
│   │   └── pipeline_step.py
│   │
│   ├── ingestion/
│   ├── quality/
│   ├── features/
│   ├── analytics/
│   ├── visualization/
│   ├── reporting/
│   ├── export/
│   ├── ml/
│   └── utils/
│
├── examples/
├── tests/
├── docs/
├── pyproject.toml
└── README.md