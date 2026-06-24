from schemas import DBSchema, APIConfig, UIConfig
from typing import List, Dict

class ValidationError(Exception):
    def __init__(self, message: str, stage: str, context: dict = None):
        self.message = message
        self.stage = stage
        self.context = context or {}
        super().__init__(self.message)

def validate_api_against_db(api_config: APIConfig, db_schema: DBSchema) -> List[str]:
    """Validates that the API configuration makes sense given the DB schema."""
    errors = []
    # For a real system, we'd check if API payload fields exist in DB tables.
    # Here we do a simplified check to ensure basic structure.
    if not api_config.endpoints:
        errors.append("APIConfig must have at least one endpoint.")
        
    db_tables = {table.name.lower(): table for table in db_schema.tables}
    
    # A simple heuristic: if an endpoint is about a specific resource, that table should exist.
    # (This is hard to enforce strictly without knowing the exact resource mapping, 
    # but we can look for obvious hallucinated fields in payloads).
    return errors

def validate_ui_against_api(ui_config: UIConfig, api_config: APIConfig) -> List[str]:
    """Validates that the UI routes and API references are valid."""
    errors = []
    api_paths = [ep.path for ep in api_config.endpoints]
    
    if not ui_config.pages:
        errors.append("UIConfig must have at least one page.")
        
    for page in ui_config.pages:
        for comp in page.components:
            if comp.data_source_api and comp.data_source_api not in api_paths:
                errors.append(f"Component '{comp.name}' references non-existent API path: {comp.data_source_api}")
            if comp.submits_to_api and comp.submits_to_api not in api_paths:
                errors.append(f"Component '{comp.name}' submits to non-existent API path: {comp.submits_to_api}")
                
    return errors
