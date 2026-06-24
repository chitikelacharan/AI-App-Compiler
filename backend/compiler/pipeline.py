import logging
from pydantic import ValidationError

from compiler.agents import (
    extract_intent,
    design_architecture,
    generate_db_schema,
    generate_api_config,
    generate_ui_config,
    generate_auth_rules
)
from compiler.validator import validate_api_against_db, validate_ui_against_api
from compiler.repair import repair_schema
from schemas import AppSchema, UIConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompilerPipeline:
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries

    def compile(self, user_prompt: str) -> AppSchema:
        logger.info("Starting compilation pipeline...")
        
        # 1. Intent Extraction
        logger.info("Stage 1: Intent Extraction")
        intent = extract_intent(user_prompt)
        
        # 2. System Design
        logger.info("Stage 2: Architecture Design")
        architecture = design_architecture(intent)
        
        # 3. DB Schema Generation
        logger.info("Stage 3: DB Schema Generation")
        db_schema = generate_db_schema(architecture)
        
        # 4. API Config Generation with Validation & Repair
        logger.info("Stage 4: API Config Generation")
        api_config = generate_api_config(architecture, db_schema)
        
        # Check custom rules
        api_errors = validate_api_against_db(api_config, db_schema)
        retries = 0
        while api_errors and retries < self.max_retries:
            logger.warning(f"API Validation failed. Repairing... Errors: {api_errors}")
            context = f"Architecture:\n{architecture.model_dump_json()}\nDB Schema:\n{db_schema.model_dump_json()}"
            # Type ignore since we use Pydantic models but dynamic class references
            api_config = repair_schema(api_config.model_dump_json(), api_errors, type(api_config), context)
            api_errors = validate_api_against_db(api_config, db_schema)
            retries += 1
            
        if api_errors:
            raise ValueError(f"Failed to repair API config after {self.max_retries} retries. Errors: {api_errors}")

        # 5. UI Config Generation with Validation & Repair
        logger.info("Stage 5: UI Config Generation")
        ui_config = generate_ui_config(architecture, api_config)
        
        ui_errors = validate_ui_against_api(ui_config, api_config)
        retries = 0
        while ui_errors and retries < self.max_retries:
            logger.warning(f"UI Validation failed. Repairing... Errors: {ui_errors}")
            context = f"Architecture:\n{architecture.model_dump_json()}\nAPI Config:\n{api_config.model_dump_json()}"
            ui_config = repair_schema(ui_config.model_dump_json(), ui_errors, type(ui_config), context)
            ui_errors = validate_ui_against_api(ui_config, api_config)
            retries += 1

        if ui_errors:
             raise ValueError(f"Failed to repair UI config after {self.max_retries} retries. Errors: {ui_errors}")

        # 6. Auth Rules Generation
        logger.info("Stage 6: Auth Rules Generation")
        auth_rules = generate_auth_rules(architecture)
        
        logger.info("Compilation successful.")
        
        return AppSchema(
            db_schema=db_schema,
            api_schema=api_config,
            ui_schema=ui_config,
            auth_rules=auth_rules
        )
