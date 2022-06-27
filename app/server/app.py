# imports
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from server.routes.person import router as PersonRouter
from fastapi.middleware.cors import CORSMiddleware

# Initialize
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(PersonRouter, tags=["Person"], prefix="/people")

# Static file serv
app.mount("/static", StaticFiles(directory="app/server/static"), name="static")
# Jinja2 Template directory
templates = Jinja2Templates(directory="app/server/templates")


@app.get("/")
def read_all_people(request: Request):
    return templates.TemplateResponse("list_people.html", {"request": request})


@app.get("/view/{id}")
def read_person(request: Request):
    return templates.TemplateResponse("view_person.html", {"request": request})


@app.get("/createui")
async def create_person_ui(request: Request):
    return templates.TemplateResponse("new_person.html", {"request": request})


@app.get("/edit/{id}")
def edit_person(request: Request):
    return templates.TemplateResponse("edit_person.html", {"request": request})
