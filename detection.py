"""Rule-based threat detection for authorized/simulated endpoint events."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    rule_id: str
    title: str
    severity: str
    confidence: float
    technique: str
    reason: str


RULES = {
    "auth.bruteforce": Detection("KD-AUTH-001", "Authentication brute-force pattern", "high", 0.94, "T1110", "Repeated authentication failures."),
    "process.suspicious": Detection("KD-EXEC-001", "Suspicious process execution", "high", 0.88, "T1059", "Execution event matched a simulated detection rule."),
    "persistence.attempt": Detection("KD-PER-001", "Persistence modification", "critical", 0.91, "T1547", "A simulated persistence change was observed."),
    "network.anomaly": Detection("KD-NET-001", "Unexpected outbound network activity", "medium", 0.79, "T1071", "Network event matched an anomaly rule."),
    "file.integrity": Detection("KD-FILE-001", "Protected file integrity change", "high", 0.86, "T1565", "Integrity event matched a simulated tampering rule."),
}


def detect(event: dict) -> Detection | None:
    return RULES.get(str(event.get("event_type")))
