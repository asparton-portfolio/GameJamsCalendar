from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import jams

# Environment setup
load_dotenv()

# App creation & configuration
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Routes
app.include_router(jams.router)

@app.get('/')
def welcome_to_api():
    return 'Welcome to Game James Calendar API! 🕹️'