from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import Base, engine, SessionLocal
from models import Student
from matching import find_match

app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


# -------------------------
# HOME
# -------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -------------------------
# SIGNUP PAGE
# -------------------------
@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {"request": request}
    )


# -------------------------
# SIGNUP SUBMIT
# -------------------------
@app.post("/signup")
async def submit_signup(
    name: str = Form(...),
    email: str = Form(...),
    country: str = Form(...),
    timezone: str = Form(...),
    interests: str = Form(...),
    languages: str = Form(...)
):
    db = SessionLocal()

    try:
        student = Student(
            name=name,
            email=email,
            country=country,
            timezone=timezone,
            interests=interests,
            languages=languages
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        match = find_match(student, db)

        # optional logging only (do NOT pass ORM to template)
        if match:
            print("Matched with:", match.name)

    finally:
        db.close()

    return RedirectResponse(url="/success", status_code=303)


# -------------------------
# STUDENTS API
# -------------------------
@app.get("/students")
async def list_students():
    db = SessionLocal()

    try:
        students = db.query(Student).all()

        return [
            {
                "name": s.name,
                "country": s.country,
                "interests": s.interests
            }
            for s in students
        ]

    finally:
        db.close()


# -------------------------
# ABOUT
# -------------------------
@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )


# -------------------------
# SUCCESS
# -------------------------
@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse(
        "success.html",
        {"request": request}
    )


# -------------------------
# DASHBOARD (FIXED CRASH SOURCE)
# -------------------------
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    db = SessionLocal()

    try:
        student = db.query(Student).order_by(Student.id.desc()).first()

        match = None
        if student:
            m = find_match(student, db)

            # convert ORM → dict safely
            if m:
                match = {
                    "name": m.name,
                    "email": m.email,
                    "country": m.country,
                    "timezone": m.timezone,
                    "interests": m.interests,
                    "languages": m.languages
                }

        student_data = None
        if student:
            student_data = {
                "name": student.name,
                "email": student.email,
                "country": student.country,
                "timezone": student.timezone,
                "interests": student.interests,
                "languages": student.languages
            }

    finally:
        db.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "student": student_data,
            "match": match
        }
    )