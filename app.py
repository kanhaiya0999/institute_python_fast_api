import os
from fastapi import FastAPI
from routes.admin.get import get_users_details
from routes.admin.post import add_class, add_pdf, add_subject, add_video
from routes.users.get import get_classes, get_pdf, get_subjects, get_video, get_videos_name
from routes.users.post import post_check_user, post_pdf_name
from routes.users.post import login_user, logout_user, register_user
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# get user end point
app.include_router(get_classes.router)
app.include_router(get_pdf.router)
app.include_router(get_subjects.router)
app.include_router(get_video.router)
app.include_router(get_videos_name.router)
app.include_router(post_check_user.router)


# post Users End point
app.include_router(login_user.router)
app.include_router(logout_user.router)
app.include_router(post_pdf_name.router)
app.include_router(register_user.router)


# get admin end point
app.include_router(get_users_details.router)


# post admin end point
app.include_router(add_class.router)
app.include_router(add_pdf.router)
app.include_router(add_subject.router)
app.include_router(add_video.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
KEY: str = os.getenv("SECRET", "")
