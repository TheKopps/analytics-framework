# Architecture

## Design Philosophy

The Analytics Framework is designed around modularity, reusability and separation of responsibilities.

The framework should remain domain-agnostic. It does not contain logic specific to supply chain, Formula 1, predictive maintenance or job market analysis.

Instead, it provides reusable building blocks that can be assembled inside domain-specific projects.

## Core Concepts

### Pipeline

The `Pipeline` class orchestrates a sequence of steps.

It does not know what each step does. It only executes them in order.

### PipelineStep

Each step inherits from `PipelineStep` and implements an `execute()` method.

This creates a common interface for all pipeline actions.

### Context

The context is a shared dictionary passed from one step to another.

It allows steps to exchange data without tightly coupling them.

Example:

```python
context["raw_data"] = ...
context["clean_data"] = ...
context["metrics"] = ...