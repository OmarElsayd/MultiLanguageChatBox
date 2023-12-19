from fastapi import FastAPI

from rtvt_services.api.login import login
from rtvt_services.api.register import register

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)