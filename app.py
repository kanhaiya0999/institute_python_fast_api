import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Import routers for admin and user
from routes.admin.get import get_users_details
from routes.admin.post import post_add_class, post_add_pdf, post_update_subject, post_add_subject, post_add_video, post_update_class
from routes.delete import delete_class, delete_subject
from routes.users.get import get_check_user, get_classes, get_pdf, get_subjects, get_pdf_name, get_video, get_videos_name
from routes.users.post import post_logout_user, post_register_user, post_login_user

app = FastAPI()

# Define GET and POST routers for user and admin
user_get_router = APIRouter(prefix="/user", tags=["User - GET"])
user_post_router = APIRouter(prefix="/user", tags=["User - POST"])
admin_get_router = APIRouter(prefix="/admin", tags=["Admin - GET"])
admin_post_router = APIRouter(prefix="/admin", tags=["Admin - POST"])
admin_delete_router = APIRouter(prefix="/admin", tags=["Admin - DELETE"])

# User GET routes
user_get_router.include_router(get_classes.router)
user_get_router.include_router(get_subjects.router)
user_get_router.include_router(get_pdf_name.router)
user_get_router.include_router(get_videos_name.router)
user_get_router.include_router(get_check_user.router)
user_get_router.include_router(get_pdf.router)
user_get_router.include_router(get_video.router)

# User POST routes
user_post_router.include_router(post_login_user.router)
user_post_router.include_router(post_logout_user.router)
user_post_router.include_router(post_register_user.router)

# Admin GET routes
admin_get_router.include_router(get_users_details.router)

# Admin POST routes
admin_post_router.include_router(post_add_class.router)
admin_post_router.include_router(post_add_pdf.router)
admin_post_router.include_router(post_add_subject.router)
admin_post_router.include_router(post_add_video.router)
admin_post_router.include_router(post_update_class.router)
admin_post_router.include_router(post_update_subject.router)

# Admin DELETE routes
admin_delete_router.include_router(delete_class.router)
admin_delete_router.include_router(delete_subject.router)

# Add routers to the main app
app.include_router(user_get_router)
app.include_router(user_post_router)
app.include_router(admin_get_router)
app.include_router(admin_post_router)
app.include_router(admin_delete_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KEY: str = os.getenv("SECRET", "")
