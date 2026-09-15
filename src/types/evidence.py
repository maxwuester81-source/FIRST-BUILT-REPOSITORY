"""
Evidence Data Structures
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class EvidenceType(Enum):
    """Classification of evidence source and type"""
    
    DIRECT = "direct"
    """Direct observation or measurement"""
    
    INDIRECT = "indirect"
    """Inferred from other observations"""
    
    CORROBORATING = "corroborating"
    """Supporting evidence from multiple sources"""


class RiskLevel(Enum):
    """Risk assessment for assumptions"""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Evidence:
    """
    Supporting evidence for a hypothesis.
    
    Quality matters: high confidence, multiple sources, verifiable.
    A single piece of evidence is insufficient for PASS.
    """
    
    evidence_id: str
    """Unique evidence identifier"""
    
    branch_id: str
    """Associated branch ID"""
    
    statement: str
    """What this evidence claims"""
    
    confidence: float
    """Confidence level (0.0-1.0)"""
    
    evidence_type: EvidenceType = EvidenceType.DIRECT
    """Type of evidence"""
    
    source: str = ""
    """Origin/source of evidence"""
    
    provenance: List[str] = field(default_factory=list)
    """Chain of reasoning leading to this evidence"""
    
    verified: bool = False
    """Whether evidence has been independently verified"""
    
    created_at: Optional[datetime] = None
    """When evidence was recorded"""
    
    metadata: dict = field(default_factory=dict)
    """Custom metadata"""
    
    def __post_init__(self):
        if not self.evidence_id or not self.branch_id:
            raise ValueError("evidence_id and branch_id are required")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be between 0.0 and 1.0")
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return (
            f"Evidence({self.evidence_id[:8]}..., "
            f"conf={self.confidence:.2f}, "
            f"type={self.evidence_type.value})"
        )


@dataclass
class Counterevidence:
    """
    Evidence that contradicts or challenges the hypothesis.
    
    Gate MUST check counterevidence quality and weight.
    Presence of counterevidence alone doesn't fail, but must be resolved.
    """
    
    counterevidence_id: str
    """Unique counterevidence identifier"""
    
    branch_id: str
    """Associated branch ID"""
    
    statement: str
    """What this counterevidence claims"""
    
    weight: float
    """Weight/severity (0.0-1.0)"""
    
    source: str = ""
    """Origin/source of counterevidence"""
    
    resolved: bool = False
    """Whether this contradiction has been addressed"""
    
    resolution: Optional[str] = None
    """How contradiction was resolved (if applicable)"""
    
    created_at: Optional[datetime] = None
    """When counterevidence was recorded"""
    
    metadata: dict = field(default_factory=dict)
    """Custom metadata"""
    
    def __post_init__(self):
        if not self.counterevidence_id or not self.branch_id:
            raise ValueError("counterevidence_id and branch_id are required")
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError("weight must be between 0.0 and 1.0")
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return (
            f"Counterevidence({self.counterevidence_id[:8]}..., "
            f"weight={self.weight:.2f}, "
            f"resolved={self.resolved})"
        )


@dataclass
class Assumption:
    """
    Core assumption a branch relies on.
    
    Gate must verify:
    - Assumptions are stated clearly
    - Risk level is assessed
    - No circular dependencies
    - Critical assumptions have evidence
    """
    
    assumption_id: str
    """Unique assumption identifier"""
    
    branch_id: str
    """Associated branch ID"""
    
    statement: str
    """The assumption claim"""
    
    risk_level: RiskLevel = RiskLevel.MEDIUM
    """How risky is this assumption?"""
    
    evidence_pointers: List[str] = field(default_factory=list)
    """Evidence supporting this assumption"""
    
    verified: bool = False
    """Whether assumption has been verified"""
    
    created_at: Optional[datetime] = None
    """When assumption was recorded"""
    
    metadata: dict = field(default_factory=dict)
    """Custom metadata"""
    
    def __post_init__(self):
        if not self.assumption_id or not self.branch_id:
            raise ValueError("assumption_id and branch_id are required")
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def is_critical(self) -> bool:
        """Check if this is a critical assumption"""
        return self.risk_level == RiskLevel.CRITICAL
    
    def __str__(self) -> str:
        return (
            f"Assumption({self.assumption_id[:8]}..., "
            f"risk={self.risk_level.value}, "
            f"verified={self.verified})"
        )
