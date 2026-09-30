# Threat Model

## Assets

- Security event integrity
- Detection rules
- API authentication token
- Local detection database
- Analyst decisions and alerts

## Threats

- Unauthenticated event injection
- Malformed or oversized payloads
- False or noisy detections
- Tampered local evidence
- Leaked API credentials

## Controls

- API-key authentication
- Source and authorization validation
- Request-size limits
- Structured event validation
- Deterministic detection rules
- Secret exclusion through .gitignore
- Automated tests and CI

Covert surveillance, credential interception, private-content collection, evasion, destructive behavior, and persistence mechanisms are outside the lab design.
