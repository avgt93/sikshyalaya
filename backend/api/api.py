from fastapi import APIRouter

from api.endpoints import (
    program,
    teacher_note,
    users,
)
from api.endpoints import login, utils, course, school, department, class_session, personal_note, user_permission

api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utils"])
api_router.include_router(school.router, prefix="/school", tags=["Schools"])
api_router.include_router(course.router, prefix="/course", tags=["Courses"])
api_router.include_router(department.router, prefix="/deparment", tags=["Departments"])
api_router.include_router(
    class_session.router, prefix="/class_session", tags=["Class Sessions"]
)
api_router.include_router(
    personal_note.router, prefix="/personal_note", tags=["Personal Notes"]
)
api_router.include_router(program.router, prefix="/program", tags=["Programs"])
api_router.include_router(user_permission.router, prefix="/user_permission", tags=["User Permission"])
api_router.include_router(
    teacher_note.router, prefix="/teacher_note", tags=["Teacher Notes"]
)