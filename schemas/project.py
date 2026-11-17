from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    project_type: str = "creative"


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    project_type: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
