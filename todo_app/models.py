from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    completed: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "12345678-1234-5678-1234-567812345678",
                "description": "Buy groceries",
                "completed": False,
            }
        }
    )
