from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Company

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "companies": companies})

@app.post("/add_company")
def add_company(
    name: str = Form(...),
    reg_number: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    new_company = Company(name=name, reg_number=reg_number, status=status)
    db.add(new_company)
    db.commit()
    return RedirectResponse("/", status_code=303)
