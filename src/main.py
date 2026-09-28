from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import init_db
from src.routers import members, projects

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(members.router)
app.include_router(projects.router)
