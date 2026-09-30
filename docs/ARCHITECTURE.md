# Architecture

KaalDrishti models a defensive endpoint-security pipeline.

## Components

- Scenario simulator: creates explicit synthetic security events.
- Ingestion API: authenticates and validates events.
- Detection engine: maps known events to detection metadata.
- Evidence store: persists normalized detections in SQLite.
- Analyst console: manually exercises scenarios and displays API responses.

## Extension path

Add correlation across events, configurable rules, alert lifecycle management, a web dashboard, pluggable storage, audit logging, and model-assisted anomaly scoring using synthetic datasets.
