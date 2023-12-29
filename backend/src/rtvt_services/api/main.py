from fastapi import FastAPI

from rtvt_services.api.login import login
from rtvt_services.api.register import register
from rtvt_services.api.rtvt_session import rtvt_session
from rtvt_services.config.google_cloud_init import GCloud

gcloud = GCloud()
gcloud.init()

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(rtvt_session.router)
