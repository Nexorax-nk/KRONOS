from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class MemoryStatus(str, Enum):
    ACTIVE = "Active"
    SUPERSEDED = "Superseded"
    DEPRECATED = "Deprecated"

class SourceType(str, Enum):
    DISCUSSION = "discussion"
    CODE = "code"
    ISSUE = "issue"
    MIGRATED = "migrated"

class Memory(BaseModel):
    id: str = Field(..., description="Unique ID of the memory, e.g., KRONOS-MEMORY-001")
    source_pr: Optional[str] = Field(None, description="Source Pull Request ID or URL")
    date: datetime = Field(default_factory=datetime.now)
    governs_files: List[str] = Field(default_factory=list, description="List of files or globs this memory governs")
    decision: str = Field(..., description="The architectural decision made")
    rejected: Optional[str] = Field(None, description="Alternatives rejected and why")
    reason: str = Field(..., description="Reasoning behind the decision")
    future_implication: Optional[str] = Field(None, description="What this means for future code")
    decided_by: List[str] = Field(..., description="GitHub handles of decision makers")
    confidence: str = Field("HIGH", description="Confidence level (LOW, MEDIUM, HIGH)")
    status: MemoryStatus = Field(MemoryStatus.ACTIVE)
    carbon_impact: Optional[str] = Field(None, description="Estimated carbon impact (e.g., ~300 kWh/month saved)")
    incident_type: Optional[str] = Field(None, description="Type of incident this relates to (e.g., retry, auth)")
    depends_on: List[str] = Field(default_factory=list, description="IDs of memories this depends on")
    blocks: List[str] = Field(default_factory=list, description="IDs of memories this blocks")
    source_type: SourceType = SourceType.DISCUSSION
    security_relevant: bool = False

    class Config:
        use_enum_values = True
