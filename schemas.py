from pydantic import BaseModel


class VersionCreate(BaseModel):
    product_id: int
    version_number: str

class ChangeLogCreate(BaseModel):
    version_id: int
    requirement_id: int
    field_name: str
    old_value: str
    new_value: str
    reason: str
    modified_by: str

class ApprovalUpdate(BaseModel):
    version_id: int
    approved_by: str
    comments: str | None = None