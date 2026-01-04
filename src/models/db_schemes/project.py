from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId 

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    @classmethod
    def validate_project_id(cls, v):
        if not v or not v.strip():
            raise ValueError('project_id cannot be empty')
        return v 

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

        @classmethod 
        def get_indexes(cls):
            return [
                {
                    "key":[
                        ("porject_id",1)
                    ],
                    "name": "project_id_index",
                    "unique": True
                }
            ]