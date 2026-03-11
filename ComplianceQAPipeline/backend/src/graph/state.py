import operator
from typing import Annotated,List,Dict,Optional,Any,TypedDict

#Define the schema for a  single compliance result
# Error Report 
class ComplianceIssue(TypedDict):
    category: str           # e.g., "FTC_DISCLOSURE"
    description: str        # Specific detail of the violation
    severity: str           # "CRITICAL" | "WARNING"
    timestamp: Optional[str]# Timestamp of occurrence (if applicable)


# 2. Define the Global Graph State
# Defines the state that gets passed around in the agentic workflow
class VideoAuditState(TypedDict):
    """
    Defines the data schema for the LangGraph execution context.
    Main container: Holds all the information about the audit right from the initial URL to the final report
    """
    # --- Input Parameters ---
    video_url: str
    video_id: str

    # --- Ingestion & Extraction Data ---
    # Optional because they are populated asynchronously by the Indexer Node.
    local_file_path: Optional[str]  
    video_metadata: Dict[str, Any]  # e.g., {"duration": 15, "resolution": "1080p"}
    transcript: Optional[str]       # Full extracted speech-to-text
    ocr_text: List[str]             # List of recognized on-screen text

    # --- Analysis Output ---
    # annotated with operator.add to allow append-only updates from multiple nodes.
    #stores the list of all violations found by ai
    compliance_results: Annotated[List[ComplianceIssue], operator.add]
    
    # --- Final Deliverables ---
    final_status: str               # "PASS" | "FAIL"
    final_report: str               # Markdown summary for the frontend
    
    # --- System Observability ---
    # Appends system-level errors (e.g., API timeouts) without halting execution logic.
    errors: Annotated[List[str], operator.add]

                                  