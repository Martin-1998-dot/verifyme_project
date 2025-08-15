from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    registration_number: str
    status: str

    class Config:
        from_attributes = True
