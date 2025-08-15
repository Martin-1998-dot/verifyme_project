from sqlalchemy.orm import Session
from models import Company
from schemas import CompanyCreate

def create_company(db: Session, company: CompanyCreate):
    db_company = Company(
        name=company.name,
        registration_number=company.registration_number,
        status=company.status
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_companies(db: Session):
    return db.query(Company).all()
