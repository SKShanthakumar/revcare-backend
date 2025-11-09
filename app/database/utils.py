from bson import ObjectId
from app.core.config import settings
from pydantic_core import core_schema 
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler 
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v, field=None):
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except Exception:
            raise ValueError("Invalid ObjectId")
    @classmethod 
    def __get_pydantic_json_schema__( cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler ) -> JsonSchemaValue:
        return {"type": "string", "pattern": "^[a-fA-F0-9]{24}$"}
