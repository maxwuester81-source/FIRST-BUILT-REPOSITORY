"""
Gate Decision Types - Output of PR_EVIDENCE_GATE_V1
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


class GateDecision(Enum):
    """
    Possible outputs from PR_EVIDENCE_GATE_V1.
    
    A successful hypothesis alone must NOT produce PASS.
    Evidence quality, provenance, and governance checks all required.
    """
    
    PASS = "PASS"
    """
    Safe to promote branch to Canon.
    All checks passed:
    - Evidence sufficient and high quality
    - Counterevidence analyzed and resolved
    - Provenance complete
    - No unresolved contradictions
    - Risk acceptable
    - Canon impact acceptable
    - Capabilities authorized
    - Resource budget compliant
    - Stopping policy respected
    - Rollback path available
    - Human approval obtained (if critical)
    """
    
    FAIL = "FAIL"
    """
    Rejection - do not promote.
    Conditions:
    - Evidence is insufficient or poor quality
    - Counterevidence contradicts hypothesis
    - Capability unauthorized
    - Resource budget exceeded
    - Stopping policy violated
    - Rollback path unavailable
    - Schema/provenance validation failed
    """
    
    BLOCKED_BY_EVIDENCE = "BLOCKED_BY_EVIDENCE"
    """
    Cannot decide yet - more evidence needed.
    Conditions:
    - Unresolved contradictions detected
    - Evidence is incomplete or unclear
    - Counterevidence not fully analyzed
    - Branch disagreement unresolved
    - Assumptions uncertain
    - Request clarification and retry
    """
    
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    """
    Technically eligible but requires human sign-off.
    Conditions:
    - Critical action (Canon merge, resource escalation, capability change)
    - High-risk decision
    - Policy requires explicit approval
    - Cannot be autonomously promoted
    """


@dataclass
class GateEvaluation:
    """Result of gate evaluation with full context"""
    
    branch_id: str
    decision: GateDecision
    reason: str
    checked_rules: List[str]
    timestamp: str
    evidence_summary: Optional[str] = None
    counterevidence_summary: Optional[str] = None
    rollback_available: bool = False
    human_approval_required: bool = False
    
    def __str__(self) -> str:
        return (
            f"GateEvaluation(branch={self.branch_id}, "
            f"decision={self.decision.value}, reason={self.reason})"
        )
