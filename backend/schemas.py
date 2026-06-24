from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

# --- 1. Intent Extraction Layer ---
class ParsedIntent(BaseModel):
    summary: str = Field(..., description="High level summary of the application")
    features: List[str] = Field(..., description="List of core features requested")
    target_users: List[str] = Field(..., description="List of target user personas")
    ambiguity_flags: List[str] = Field(
        default_factory=list,
        description="Vague, conflicting, or missing requirements detected in the prompt"
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="Explicit assumptions made to fill gaps or resolve ambiguity"
    )

# --- 2. System Design Layer ---
class Entity(BaseModel):
    name: str = Field(..., description="Name of the entity, e.g., 'User', 'Product'")
    description: str = Field(..., description="What this entity represents")

class UserRole(BaseModel):
    role_name: str = Field(..., description="Name of the role, e.g., 'Admin', 'Customer'")
    description: str = Field(..., description="What this role can do")

class UserFlow(BaseModel):
    name: str = Field(..., description="Name of the flow, e.g., 'Checkout Process'")
    steps: List[str] = Field(..., description="Sequence of actions in the flow")

class AppArchitecture(BaseModel):
    entities: List[Entity]
    roles: List[UserRole]
    flows: List[UserFlow]

# --- 3. Schema Generation Layer ---

# DB Schema
class Column(BaseModel):
    name: str
    type: Literal["string", "integer", "float", "boolean", "datetime", "uuid"]
    is_primary_key: bool = False
    is_nullable: bool = False
    foreign_key_to: Optional[str] = Field(None, description="Format: 'table_name.column_name'")

class Table(BaseModel):
    name: str = Field(..., description="Pluralized table name")
    columns: List[Column]

class DBSchema(BaseModel):
    tables: List[Table]

# API Schema
class APIPayloadField(BaseModel):
    name: str
    type: Literal["string", "integer", "float", "boolean", "datetime", "uuid", "array", "object"]
    is_required: bool

class APIEndpoint(BaseModel):
    path: str = Field(..., description="E.g., '/api/v1/users'")
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    description: str
    requires_auth: bool
    allowed_roles: List[str] = Field(default_factory=list)
    request_payload: Optional[List[APIPayloadField]] = None
    response_payload: Optional[List[APIPayloadField]] = None

class APIConfig(BaseModel):
    endpoints: List[APIEndpoint]

# UI Schema
class UIComponent(BaseModel):
    name: str = Field(..., description="Component name, e.g., 'LoginForm'")
    type: Literal["form", "table", "list", "dashboard", "card", "hero"]
    data_source_api: Optional[str] = Field(None, description="API endpoint path if it fetches data")
    submits_to_api: Optional[str] = Field(None, description="API endpoint path if it submits data")

class UIPage(BaseModel):
    route: str = Field(..., description="E.g., '/dashboard'")
    title: str
    components: List[UIComponent]
    requires_auth: bool
    allowed_roles: List[str] = Field(default_factory=list)

class UIConfig(BaseModel):
    pages: List[UIPage]

# Auth Rules
class AuthRules(BaseModel):
    enabled: bool = True
    roles: List[str]
    default_role: str

# Final App Schema
class AppSchema(BaseModel):
    db_schema: DBSchema
    api_schema: APIConfig
    ui_schema: UIConfig
    auth_rules: AuthRules
    assumptions: List[str] = Field(
        default_factory=list,
        description="All assumptions made during compilation and repair"
    )
    validation_warnings: List[str] = Field(
        default_factory=list,
        description="Non-fatal validation issues detected (may have been auto-repaired)"
    )
