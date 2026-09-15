"""
Database migrations and schema initialization for COA Epistemic Ledger.

Provides database schema setup, versioning, and migration support.
"""

import sqlite3
from pathlib import Path
from typing import Optional


# Current schema version
SCHEMA_VERSION = 1


def get_schema_sql() -> str:
    """
    Complete SQL schema for COA Epistemic Ledger V1.
    
    Tables:
    - branches: Core ledger of hypothesis branches
    - evidence: Supporting evidence for branches
    - counterevidence: Contradicting evidence
    - assumptions: Core assumptions of branches
    - provenance_entries: Full decision history
    - gate_decisions: Audit trail of gate evaluations
    - schema_version: Schema version tracking
    """
    return """
-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Branches: Core ledger
CREATE TABLE IF NOT EXISTS branches (
    branch_id TEXT PRIMARY KEY,
    parent_id TEXT,
    task_id TEXT,
    hypothesis TEXT NOT NULL,
    branch_type TEXT DEFAULT 'hypothesis',
    owner_agent_id TEXT,
    status TEXT DEFAULT 'active',
    progress_score REAL DEFAULT 0.0,
    resource_allocation REAL DEFAULT 0.0,
    resource_consumption REAL DEFAULT 0.0,
    pruning_reason TEXT,
    merge_target TEXT,
    resource_action TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    FOREIGN KEY(parent_id) REFERENCES branches(branch_id),
    CHECK(progress_score >= 0.0 AND progress_score <= 1.0),
    CHECK(resource_consumption >= 0.0),
    CHECK(resource_allocation >= 0.0)
);

-- Evidence: Supporting evidence
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id TEXT PRIMARY KEY,
    branch_id TEXT NOT NULL,
    statement TEXT NOT NULL,
    confidence REAL NOT NULL,
    evidence_type TEXT DEFAULT 'direct',
    source TEXT DEFAULT '',
    verified INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id),
    CHECK(confidence >= 0.0 AND confidence <= 1.0)
);

-- Counterevidence: Contradicting evidence
CREATE TABLE IF NOT EXISTS counterevidence (
    counterevidence_id TEXT PRIMARY KEY,
    branch_id TEXT NOT NULL,
    statement TEXT NOT NULL,
    weight REAL NOT NULL,
    source TEXT DEFAULT '',
    resolved INTEGER DEFAULT 0,
    resolution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id),
    CHECK(weight >= 0.0 AND weight <= 1.0)
);

-- Assumptions: Core assumptions
CREATE TABLE IF NOT EXISTS assumptions (
    assumption_id TEXT PRIMARY KEY,
    branch_id TEXT NOT NULL,
    statement TEXT NOT NULL,
    risk_level TEXT DEFAULT 'medium',
    verified INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
);

-- Provenance: Full decision history chain
CREATE TABLE IF NOT EXISTS provenance_entries (
    entry_id TEXT PRIMARY KEY,
    branch_id TEXT NOT NULL,
    chain_index INTEGER NOT NULL,
    element_type TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
);

-- Gate Decisions: Audit trail
CREATE TABLE IF NOT EXISTS gate_decisions (
    decision_id TEXT PRIMARY KEY,
    branch_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    reason TEXT NOT NULL,
    checked_rules TEXT,
    rollback_available INTEGER DEFAULT 0,
    human_approval_required INTEGER DEFAULT 0,
    evidence_summary TEXT,
    counterevidence_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
);

-- Indices for query performance
CREATE INDEX IF NOT EXISTS idx_branches_parent_id ON branches(parent_id);
CREATE INDEX IF NOT EXISTS idx_branches_task_id ON branches(task_id);
CREATE INDEX IF NOT EXISTS idx_branches_status ON branches(status);
CREATE INDEX IF NOT EXISTS idx_branches_owner_agent_id ON branches(owner_agent_id);
CREATE INDEX IF NOT EXISTS idx_branches_created_at ON branches(created_at);

CREATE INDEX IF NOT EXISTS idx_evidence_branch_id ON evidence(branch_id);
CREATE INDEX IF NOT EXISTS idx_counterevidence_branch_id ON counterevidence(branch_id);
CREATE INDEX IF NOT EXISTS idx_assumptions_branch_id ON assumptions(branch_id);
CREATE INDEX IF NOT EXISTS idx_provenance_branch_id ON provenance_entries(branch_id);
CREATE INDEX IF NOT EXISTS idx_gate_decisions_branch_id ON gate_decisions(branch_id);
"""


def init_database(db_path: str) -> sqlite3.Connection:
    """
    Initialize database with schema.
    
    Args:
        db_path: Path to SQLite database file
        
    Returns:
        Database connection
        
    Raises:
        sqlite3.DatabaseError: If schema initialization fails
    """
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like row access
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    conn.execute("PRAGMA journal_mode = WAL")  # Write-ahead logging for safety
    
    try:
        # Create schema
        conn.executescript(get_schema_sql())
        
        # Initialize schema version if not present
        cursor = conn.cursor()
        cursor.execute("SELECT version FROM schema_version LIMIT 1")
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO schema_version (version) VALUES (?)",
                (SCHEMA_VERSION,)
            )
        
        conn.commit()
        return conn
    
    except sqlite3.DatabaseError as e:
        conn.close()
        raise sqlite3.DatabaseError(f"Failed to initialize database: {e}")


def get_schema_version(conn: sqlite3.Connection) -> int:
    """
    Get current schema version.
    
    Args:
        conn: Database connection
        
    Returns:
        Schema version number
    """
    cursor = conn.cursor()
    cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
    result = cursor.fetchone()
    return result[0] if result else 0


def migrate_database(conn: sqlite3.Connection, target_version: Optional[int] = None) -> int:
    """
    Migrate database to target version.
    
    Currently supports only version 1 (initial schema).
    Future versions would implement incremental migrations.
    
    Args:
        conn: Database connection
        target_version: Target schema version (None = current SCHEMA_VERSION)
        
    Returns:
        Final schema version
    """
    if target_version is None:
        target_version = SCHEMA_VERSION
    
    current_version = get_schema_version(conn)
    
    if current_version == target_version:
        return current_version
    
    if current_version > target_version:
        raise ValueError(
            f"Cannot downgrade from v{current_version} to v{target_version}"
        )
    
    # Version 1 is initial schema - no migration needed
    if target_version == 1:
        return current_version
    
    raise NotImplementedError(f"Migration to version {target_version} not implemented")
