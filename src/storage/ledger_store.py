"""
Abstract ledger store interface.

Defines the contract for persistent branch ledger storage.
Can be implemented by different backends (SQLite, PostgreSQL, etc.).
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.types.branch import Branch, BranchStatus
from src.types.evidence import Evidence, Counterevidence, Assumption
from src.types.decisions import GateEvaluation


class LedgerStore(ABC):
    """
    Abstract interface for persistent branch ledger storage.
    
    All operations are transactional and must preserve:
    - Branch history (including falsified/pruned branches)
    - Provenance chain completeness
    - ACID compliance
    - Foreign key integrity
    """
    
    # ==================== Branch Operations ====================
    
    @abstractmethod
    def create_branch(self, branch: Branch) -> bool:
        """
        Persist a new branch to ledger.
        
        Args:
            branch: Branch object to persist
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If branch_id already exists or validation fails
        """
        pass
    
    @abstractmethod
    def get_branch(self, branch_id: str) -> Optional[Branch]:
        """
        Retrieve branch by ID (including falsified/pruned branches).
        
        Args:
            branch_id: Unique branch identifier
            
        Returns:
            Branch object or None if not found
        """
        pass
    
    @abstractmethod
    def get_branches_by_parent(self, parent_id: str) -> List[Branch]:
        """
        Get all child branches of a parent.
        
        Args:
            parent_id: Parent branch ID
            
        Returns:
            List of child branches
        """
        pass
    
    @abstractmethod
    def get_branches_by_task(self, task_id: str) -> List[Branch]:
        """
        Get all branches associated with a task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            List of branches for task
        """
        pass
    
    @abstractmethod
    def get_branches_by_status(self, status: BranchStatus) -> List[Branch]:
        """
        Get all branches with specific status.
        
        Args:
            status: Branch status (active, falsified, pruned, merged)
            
        Returns:
            List of branches with status
        """
        pass
    
    @abstractmethod
    def update_branch(self, branch: Branch) -> bool:
        """
        Update existing branch.
        
        Args:
            branch: Updated branch object
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If branch_id doesn't exist
        """
        pass
    
    @abstractmethod
    def list_all_branches(self, include_pruned: bool = True) -> List[Branch]:
        """
        Get all branches in ledger.
        
        Args:
            include_pruned: Whether to include pruned branches (default True)
            
        Returns:
            List of all branches
        """
        pass
    
    # ==================== Evidence Operations ====================
    
    @abstractmethod
    def create_evidence(self, evidence: Evidence) -> bool:
        """
        Persist evidence for a branch.
        
        Args:
            evidence: Evidence object
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """
        Retrieve evidence by ID.
        
        Args:
            evidence_id: Evidence identifier
            
        Returns:
            Evidence object or None
        """
        pass
    
    @abstractmethod
    def get_evidence_by_branch(self, branch_id: str) -> List[Evidence]:
        """
        Get all evidence for a branch.
        
        Args:
            branch_id: Branch identifier
            
        Returns:
            List of evidence for branch
        """
        pass
    
    @abstractmethod
    def update_evidence(self, evidence: Evidence) -> bool:
        """
        Update existing evidence.
        
        Args:
            evidence: Updated evidence object
            
        Returns:
            True if successful
        """
        pass
    
    # ==================== Counterevidence Operations ====================
    
    @abstractmethod
    def create_counterevidence(self, counterevidence: Counterevidence) -> bool:
        """
        Persist counterevidence for a branch.
        
        Args:
            counterevidence: Counterevidence object
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def get_counterevidence(self, counterevidence_id: str) -> Optional[Counterevidence]:
        """
        Retrieve counterevidence by ID.
        
        Args:
            counterevidence_id: Counterevidence identifier
            
        Returns:
            Counterevidence object or None
        """
        pass
    
    @abstractmethod
    def get_counterevidence_by_branch(self, branch_id: str) -> List[Counterevidence]:
        """
        Get all counterevidence for a branch.
        
        Args:
            branch_id: Branch identifier
            
        Returns:
            List of counterevidence for branch
        """
        pass
    
    @abstractmethod
    def update_counterevidence(self, counterevidence: Counterevidence) -> bool:
        """
        Update existing counterevidence.
        
        Args:
            counterevidence: Updated counterevidence object
            
        Returns:
            True if successful
        """
        pass
    
    # ==================== Assumption Operations ====================
    
    @abstractmethod
    def create_assumption(self, assumption: Assumption) -> bool:
        """
        Persist assumption for a branch.
        
        Args:
            assumption: Assumption object
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def get_assumption(self, assumption_id: str) -> Optional[Assumption]:
        """
        Retrieve assumption by ID.
        
        Args:
            assumption_id: Assumption identifier
            
        Returns:
            Assumption object or None
        """
        pass
    
    @abstractmethod
    def get_assumptions_by_branch(self, branch_id: str) -> List[Assumption]:
        """
        Get all assumptions for a branch.
        
        Args:
            branch_id: Branch identifier
            
        Returns:
            List of assumptions for branch
        """
        pass
    
    @abstractmethod
    def update_assumption(self, assumption: Assumption) -> bool:
        """
        Update existing assumption.
        
        Args:
            assumption: Updated assumption object
            
        Returns:
            True if successful
        """
        pass
    
    # ==================== Provenance Operations ====================
    
    @abstractmethod
    def add_provenance_entry(
        self,
        branch_id: str,
        chain_index: int,
        element_type: str,
        content: str,
        source: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add entry to provenance chain.
        
        Args:
            branch_id: Associated branch ID
            chain_index: Position in chain (incremental)
            element_type: Type (assumption, evidence, counterevidence, action)
            content: Entry content
            source: Origin of entry
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def get_provenance_chain(self, branch_id: str) -> List[Dict[str, Any]]:
        """
        Get full provenance chain for branch (ordered).
        
        Args:
            branch_id: Branch identifier
            
        Returns:
            List of provenance entries in order
        """
        pass
    
    # ==================== Gate Decision Operations ====================
    
    @abstractmethod
    def record_gate_decision(self, evaluation: GateEvaluation) -> bool:
        """
        Record gate evaluation decision.
        
        Args:
            evaluation: GateEvaluation result
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    def get_gate_decisions_for_branch(self, branch_id: str) -> List[GateEvaluation]:
        """
        Get all gate decisions for a branch (audit trail).
        
        Args:
            branch_id: Branch identifier
            
        Returns:
            List of gate decisions in chronological order
        """
        pass
    
    # ==================== Query Operations ====================
    
    @abstractmethod
    def get_branch_hierarchy(self, root_branch_id: str) -> Dict[str, Any]:
        """
        Get full branch hierarchy tree starting from root.
        
        Args:
            root_branch_id: Root branch identifier
            
        Returns:
            Hierarchical representation of branch tree
        """
        pass
    
    @abstractmethod
    def search_branches(self, filters: Dict[str, Any]) -> List[Branch]:
        """
        Search branches using arbitrary filters.
        
        Supported filters:
        - status: BranchStatus or list of statuses
        - owner_agent_id: Agent identifier
        - task_id: Task identifier
        - hypothesis: Text search (substring)
        - min_progress_score: Minimum score (0.0-1.0)
        - created_after: Datetime
        - created_before: Datetime
        
        Args:
            filters: Search filters
            
        Returns:
            List of matching branches
        """
        pass
    
    # ==================== Lifecycle ====================
    
    @abstractmethod
    def close(self):
        """Close database connection and cleanup resources."""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify database is accessible and schema is valid.
        
        Returns:
            True if healthy
        """
        pass
