# Changelog

## 2026-09-30 — Modernization

- Reworked the client around synthetic, consent-based security events.
- Replaced legacy ingestion with authenticated JSON event ingestion.
- Added request-size limits and strict synthetic-event validation.
- Reworked the GUI into an explicit manual test-event tool.
- Added pytest coverage for health, authentication, validation, and ingestion.
- Added environment-backed configuration and .env.example.
- Added CI and CodeQL workflows.
- Removed legacy surveillance-oriented collection and persistence components.
- Refreshed project documentation.
