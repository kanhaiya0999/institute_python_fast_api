import datetime
import os
import random
from bson import ObjectId
from fastapi import FastAPI, File, Request, Response
import jwt
from pydantic import BaseModel, EmailStr, Field
from connect_db import get_class_collection, get_pdf_collection, get_subject_collection, get_user_collection, get_video_collection
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specific domains ko restrict kar sakte ho
    allow_credentials=True,
    # Ya phir ["POST", "GET", "OPTIONS"] specify kar sakte ho
    allow_methods=["*"],
    allow_headers=["*"],
)
KEY = os.getenv("SECRET")


class UserRegisterTypes(BaseModel):
    name: str
    email: EmailStr
    phone: int
    password: str
    type: str = "user"
    jwt: str | None = None
    jwt_expire: str | None = None


class SubjectsTypes(BaseModel):
    class_name_id: str = Field(max_length=24, min_length=24)
    name: str


class GetSubjectsTypes(BaseModel):
    class_name_id: str


class PDFsTypes(BaseModel):
    subject_object_id: str
    name: str
    pdf: bytes = File(media_type="application/pdf")


class GetPDFsTypesName(BaseModel):
    subject_object_id: str


class GetPdfFileType(BaseModel):
    pdf_object_id: str


class VideoTypes(BaseModel):
    subject_object_id: str
    name: str
    video: bytes = File(media_type="video/mp4")


class GetVideoNameTypes(BaseModel):
    video_object_id: str


class GetVideoTypes(BaseModel):
    video_object_id: str


class ClassesTypes(BaseModel):
    name: str
    desc: str
    price: int


class UserLoginTypes(BaseModel):
    email: EmailStr
    password: str


@app.post("/api/register")
async def register_user(details: UserRegisterTypes):
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    users_collection = await get_user_collection()
    user_details = users_collection.find_one({"email": details.email})
    if user_details is not None:
        return {"status": 200, "message": "User Already Created", "is_success": False}

    users_collection.insert_one(details.model_dump())
    return {"status": 200, "message": "User Created", "is_success": True}


@app.post("/api/login")
async def login_user(details: UserLoginTypes, response: Response):
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}

    users_collection = await get_user_collection()
    user_details = users_collection.find_one({"email": details.email})

    if (user_details is None or user_details["password"] != details.password):
        return {"status": 404, "message": "User Not Found or invalid email or password", "is_success": False}
    current_time = datetime.datetime.now(datetime.timezone.utc)
    print(current_time)
    expiry_time = current_time + \
        datetime.timedelta(hours=1)

    jwt_details = {
        "email": user_details["email"],
        "random": random.random(),
        "time": current_time.timestamp(),
        "exp": expiry_time
    }

    encoded_jwt = jwt.encode(jwt_details, KEY, algorithm="HS256")
    user_details["jwt"] = encoded_jwt
    user_details["jwt_expire"] = expiry_time
    users_collection.update_one({"email": details.email}, {
                                "$set": {"jwt": encoded_jwt, "jwt_expire": expiry_time}})
    response.set_cookie(key="jwt", value=encoded_jwt, httponly=True)
    return {"status": 200, "message": "User Logged In", "is_success": True, "jwt": encoded_jwt}


@app.post("/api/add_class")
async def add_class(details: ClassesTypes, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}

    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)

    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}, "type": "admin"})
    print(user_details)
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    classes_collection = await get_class_collection()
    classes_collection.insert_one(details.model_dump())
    return {"status": 200, "message": "Class Added", "is_success": True}


@app.post("/api/logout")
async def logout_user(request: Request, response: Response):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    user_details = user_collection.find_one({"jwt": user_jwt})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}

    user_collection.update_one({"jwt": user_jwt}, {
        "$set": {"jwt": None, "jwt_expire": None}})

    response.delete_cookie(key="jwt")
    return {"status": 200, "message": "User Logged Out", "is_success": True}


@app.get("/api/get_classes")
async def get_classes(request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    classes_collection = await get_class_collection()
    classes = classes_collection.find()

    classes = [dict(class_details, _id=str(class_details["_id"]))
               for class_details in classes]
    return {"status": 200, "message": "Classes Fetched", "is_success": True, "classes": list(classes)}


@app.post("/api/add_subject")
async def add_subject(details: SubjectsTypes, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}, "type": "admin"})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    classes_collection = await get_class_collection()
    class_details = classes_collection.find_one(
        {"_id": ObjectId(details.class_name_id)})
    if class_details is None:
        return {"status": 404, "message": "Class Not Found", "is_success": False}

    classes_collection = await get_subject_collection()
    classes_collection.insert_one(details.model_dump())
    return {"status": 200, "message": "Subject Added", "is_success": True}


@app.post("/api/get_subjects")
async def get_subjects(details: GetSubjectsTypes, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    subjects_collection = await get_subject_collection()
    subjects = subjects_collection.find(
        {"class_name_id": details.class_name_id})

    subjects = [dict(subject_details, _id=str(subject_details["_id"]))
                for subject_details in subjects]
    return {"status": 200, "message": "Subjects Fetched", "is_success": True, "subjects": list(subjects)}


@app.post("/api/add_pdf")
async def add_pdf(details: PDFsTypes, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}, "type": "admin"})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    subjects_collection = await get_subject_collection()
    subject_details = subjects_collection.find_one(
        {"_id": ObjectId(details.subject_object_id)})
    if subject_details is None:
        return {"status": 404, "message": "Subject Not Found", "is_success": False}
    pdfs_collection = await get_pdf_collection()
    pdfs_collection.insert_one(details.model_dump())
    return {"status": 200, "message": "PDF Added", "is_success": True}


@app.get("/api/get_pdfs_name")
async def get_pdfs_name(details: GetPDFsTypesName, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    pdfs_collection = await get_pdf_collection()
    pdfs = pdfs_collection.find(
        {"subject_object_id": details.subject_object_id}, {"pdf": False})
    print(pdfs)
    pdfs = [dict(pdf_details, _id=str(pdf_details["_id"]))
            for pdf_details in pdfs]
    return {"status": 200, "message": "PDFs Fetched", "is_success": True, "pdfs": list(pdfs)}


@app.get("/api/get_pdf")
async def get_pdf(details: GetPdfFileType, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    pdfs_collection = await get_pdf_collection()
    pdf_details = pdfs_collection.find_one(
        {"_id": ObjectId(details.pdf_object_id)})
    if pdf_details is None:
        return {"status": 404, "message": "PDF Not Found", "is_success": False}

    pdf_details = dict(pdf_details, _id=str(pdf_details["_id"]))

    return {"status": 200, "message": "PDF Fetched", "is_success": True, "pdf": pdf_details}


@app.post("/api/add_video")
async def add_video(details: VideoTypes, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}, "type": "admin"})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    subjects_collection = await get_subject_collection()
    subject_details = subjects_collection.find_one(
        {"_id": ObjectId(details.subject_object_id)})
    if subject_details is None:
        return {"status": 404, "message": "Subject Not Found", "is_success": False}
    videos_collection = await get_video_collection()
    videos_collection.insert_one(details.model_dump())
    return {"status": 200, "message": "Video Added", "is_success": True}


@app.get("/api/get_videos_name")
async def get_videos_name(details: GetVideoNameTypes, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    videos_collection = await get_video_collection()
    videos = videos_collection.find(
        {"subject_object_id": details.video_object_id}, {"video": False})
    print(videos)
    videos = [dict(video_details, _id=str(video_details["_id"]))
              for video_details in videos]
    return {"status": 200, "message": "Videos Fetched", "is_success": True, "videos": list(videos)}


@app.get("/api/get_video")
async def get_video(details: GetVideoTypes, request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    videos_collection = await get_video_collection()
    video_details = videos_collection.find_one(
        {"_id": ObjectId(details.video_object_id)})
    if video_details is None:
        return {"status": 404, "message": "Video Not Found", "is_success": False}

    video_details = dict(video_details, _id=str(video_details["_id"]))

    return {"status": 200, "message": "Video Fetched", "is_success": True, "video": video_details}


@app.get("/api/get_users_details")
async def get_users_details(request: Request):
    user_jwt = request.headers.get('x-auth-token')
    if not user_jwt:
        return {"status": 401, "message": "Unauthorized", "is_success": False}
    if KEY is None:
        return {"status": 500, "message": "SECRET key not found in environment", "is_success": False}
    user_collection = await get_user_collection()
    current_date = datetime.datetime.now(datetime.timezone.utc)
    user_details = user_collection.find_one(
        {"jwt": user_jwt, "jwt_expire": {"$gte": current_date}, "type": "admin"})
    if user_details is None:
        return {"status": 404, "message": "User Not Found", "is_success": False}
    all_users = user_collection.find()
    all_users = [dict(user_details, _id=str(user_details["_id"]))
                 for user_details in all_users]
    return {"status": 200, "message": "Users Fetched", "is_success": True, "users": list(all_users)}
