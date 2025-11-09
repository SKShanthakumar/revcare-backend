from bson import ObjectId
from app.core.config import settings
from pydantic_core import core_schema 
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler 
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    """
    Custom Pydantic-compatible ObjectId type for MongoDB.
    
    This class allows MongoDB ObjectIds to be used seamlessly with Pydantic models,
    providing validation and JSON schema generation.
    """
    
    @classmethod
    def __get_validators__(cls):
        """
        Get validators for Pydantic field validation.
        
        Yields:
            callable: The validate method for field validation
        """
        yield cls.validate
    
    @classmethod
    def validate(cls, v, field=None):
        """
        Validate and convert a value to ObjectId.
        
        Args:
            v: Value to validate (can be ObjectId, string, or other)
            field: Optional Pydantic field (not used)
            
        Returns:
            ObjectId: Valid ObjectId instance
            
        Raises:
            ValueError: If the value cannot be converted to a valid ObjectId
        """
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except Exception:
            raise ValueError("Invalid ObjectId")
    
    @classmethod 
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        """
        Generate JSON schema for this ObjectId type.
        
        Args:
            schema: Core schema from Pydantic
            handler: JSON schema handler
            
        Returns:
            JsonSchemaValue: JSON schema dictionary with type and pattern
        """
        return {"type": "string", "pattern": "^[a-fA-F0-9]{24}$"}
