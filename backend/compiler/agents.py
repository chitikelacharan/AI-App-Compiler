import os
import json
from google import genai
from google.genai import types
from schemas import ParsedIntent, AppArchitecture, AppSchema, DBSchema, APIConfig, UIConfig, AuthRules

# Initialize Gemini client lazily
def get_client():
    try:
        return genai.Client()
    except ValueError:
        return None

MODEL_NAME = "gemini-2.5-flash" # Use a fast model for the pipeline

def generate_mock_for_schema(schema_class):
    """Generates a highly simplified mock response based on the schema for demo purposes when no API key is present."""
    if schema_class == ParsedIntent:
        return ParsedIntent(summary="Mock App", features=["Feature 1", "Feature 2"], target_users=["Users", "Admins"])
    elif schema_class == AppArchitecture:
        from schemas import Entity, UserRole, UserFlow
        return AppArchitecture(
            entities=[Entity(name="User", description="A user")],
            roles=[UserRole(role_name="Admin", description="Admin role")],
            flows=[UserFlow(name="Login", steps=["Enter creds"])]
        )
    elif schema_class == DBSchema:
        from schemas import Table, Column
        return DBSchema(tables=[Table(name="users", columns=[Column(name="id", type="integer", is_primary_key=True)])])
    elif schema_class == APIConfig:
        from schemas import APIEndpoint
        return APIConfig(endpoints=[APIEndpoint(path="/api/users", method="GET", description="Get users", requires_auth=False)])
    elif schema_class == UIConfig:
        from schemas import UIPage, UIComponent
        return UIConfig(pages=[UIPage(route="/", title="Home", components=[UIComponent(name="List", type="list", data_source_api="/api/users")], requires_auth=False)])
    elif schema_class == AuthRules:
        return AuthRules(enabled=True, roles=["Admin"], default_role="Admin")
    return None

def call_llm_with_schema(prompt: str, schema_class, system_instruction: str = None):
    """Generic wrapper for calling Gemini with a structured output schema."""
    client = get_client()
    if not client:
        return generate_mock_for_schema(schema_class)

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schema_class,
        temperature=0.1,
    )
    if system_instruction:
        config.system_instruction = system_instruction
        
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    
    # Parse the returned JSON string into the Pydantic model
    return schema_class.model_validate_json(response.text)

def extract_intent(user_prompt: str) -> ParsedIntent:
    system_instruction = "You are an expert product manager. Extract the core intent, features, and target users from the user's software description."
    return call_llm_with_schema(user_prompt, ParsedIntent, system_instruction)

def design_architecture(intent: ParsedIntent) -> AppArchitecture:
    system_instruction = "You are an expert system architect. Given the product intent, design the high-level architecture including entities, user roles, and core user flows."
    prompt = f"Intent Summary: {intent.summary}\nFeatures: {', '.join(intent.features)}\nTarget Users: {', '.join(intent.target_users)}"
    return call_llm_with_schema(prompt, AppArchitecture, system_instruction)

def generate_db_schema(architecture: AppArchitecture) -> DBSchema:
    system_instruction = "You are a database architect. Generate a relational database schema for the provided architecture. Ensure all entities have corresponding tables. Use plural names for tables."
    prompt = architecture.model_dump_json()
    return call_llm_with_schema(prompt, DBSchema, system_instruction)

def generate_api_config(architecture: AppArchitecture, db_schema: DBSchema) -> APIConfig:
    system_instruction = "You are a backend engineer. Generate a RESTful API specification that serves the required flows and interacts with the provided DB schema. Ensure endpoints have payload definitions."
    prompt = f"Architecture:\n{architecture.model_dump_json()}\n\nDB Schema:\n{db_schema.model_dump_json()}"
    return call_llm_with_schema(prompt, APIConfig, system_instruction)

def generate_ui_config(architecture: AppArchitecture, api_config: APIConfig) -> UIConfig:
    system_instruction = "You are a frontend engineer. Generate a UI page and component structure that matches the user flows. Bind UI components to the provided API endpoints where data fetching or submission is needed."
    prompt = f"Architecture:\n{architecture.model_dump_json()}\n\nAPI Schema:\n{api_config.model_dump_json()}"
    return call_llm_with_schema(prompt, UIConfig, system_instruction)

def generate_auth_rules(architecture: AppArchitecture) -> AuthRules:
    system_instruction = "You are a security engineer. Generate authorization rules based on the user roles and flows."
    prompt = f"Architecture:\n{architecture.model_dump_json()}"
    return call_llm_with_schema(prompt, AuthRules, system_instruction)
