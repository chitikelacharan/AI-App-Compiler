from google import genai
from google.genai import types
from schemas import DBSchema, APIConfig, UIConfig, AuthRules
import json
import os

def get_client():
    try:
        return genai.Client()
    except ValueError:
        return None

MODEL_NAME = "gemini-2.5-flash"

def repair_schema(failed_json: str, errors: list[str], target_schema_class, context_instruction: str):
    """
    Takes a failing JSON output, the list of validation errors, and asks the LLM to fix it.
    Returns a parsed and validated Pydantic model.
    """
    system_instruction = (
        "You are an expert system repair agent. The previous generation failed validation. "
        "Your job is to read the validation errors, the previous JSON output, and the context, "
        "and return a completely valid JSON that fixes the issues while keeping the rest intact."
    )
    
    prompt = f"""
Context:
{context_instruction}

Previous Output (Failed):
{failed_json}

Validation Errors to Fix:
{json.dumps(errors, indent=2)}

Please generate the corrected JSON.
"""

    client = get_client()
    if not client:
        # In mock mode, just return the previously failed JSON (or you could attempt to parse and default)
        try:
            return target_schema_class.model_validate_json(failed_json)
        except:
            # If it's totally broken in mock mode, return a generic mock
            from compiler.agents import generate_mock_for_schema
            return generate_mock_for_schema(target_schema_class)

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=target_schema_class,
        system_instruction=system_instruction,
        temperature=0.1,
    )
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    
    return target_schema_class.model_validate_json(response.text)
