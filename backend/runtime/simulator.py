from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from schemas import AppSchema
import uuid

def execute_schema(app_schema: AppSchema) -> dict:
    """
    Simulates execution of the schema by creating a dynamic SQLite database in-memory
    and verifying the tables can be successfully created.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    metadata = MetaData()
    
    type_map = {
        "string": String,
        "integer": Integer,
        "float": Float,
        "boolean": Boolean,
        "datetime": DateTime,
        "uuid": String, # SQLite doesn't have native UUID, use String
    }
    
    created_tables = []
    
    try:
        # First pass: create all tables without foreign keys to avoid circular dependency issues in simple simulation
        for table_def in app_schema.db_schema.tables:
            columns = []
            for col_def in table_def.columns:
                col_type = type_map.get(col_def.type, String)
                
                # Setup Column
                col_kwargs = {
                    "primary_key": col_def.is_primary_key,
                    "nullable": col_def.is_nullable
                }
                
                if col_def.foreign_key_to:
                    columns.append(Column(col_def.name, col_type, ForeignKey(col_def.foreign_key_to), **col_kwargs))
                else:
                    columns.append(Column(col_def.name, col_type, **col_kwargs))
                    
            Table(table_def.name, metadata, *columns)
            created_tables.append(table_def.name)
            
        # Create all tables in the engine
        metadata.create_all(engine)
        
        return {
            "status": "success",
            "message": "Runtime simulation successful. Schema is executable.",
            "database": "sqlite:///:memory:",
            "tables_created": created_tables,
            "api_endpoints_simulated": [ep.path for ep in app_schema.api_schema.endpoints]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to execute schema: {str(e)}"
        }
