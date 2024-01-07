from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware


from rtvt_services.dependency.user_checker import get_curr_user
from rtvt_services.util.constant import API_V1_BASE_ROOT
from rtvt_services.api.chat import chat
from rtvt_services.api.login import login
from rtvt_services.api.register import register
from rtvt_services.api.rtvt_session import rtvt_session
from rtvt_services.config.google_cloud_init import GCloud

gcloud = GCloud()
gcloud.init()

app = FastAPI(
    title="Multi Language Chat Box API",
    version='0.1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(
    f"{API_V1_BASE_ROOT}/verify_access",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_curr_user)]
)
async def verify_access():
    return True


app.include_router(register.router)
app.include_router(login.router)
app.include_router(rtvt_session.router)
app.include_router(chat.router)
