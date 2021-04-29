from typing import Any

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Request,
)
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import cruds
import models
import schemas
from core import throttle
from core.security import get_password_hash, create_sesssion_token
from forms.login import LoginForm
from utils import deps
from utils.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/auth/web", response_model=schemas.Token)
async def login_web_session(
        db: Session = Depends(deps.get_db), form_data: LoginForm = Depends()
) -> Any:
    if not form_data.username:
        form_data.username = form_data.email

    user = cruds.crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    session_token = await create_sesssion_token(user, form_data.remember_me)
    response = JSONResponse({"status": "success"})
    response.set_cookie("session", session_token, httponly=True)
    return response


@router.get("/auth/web/test")
async def test_session_token(
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    return current_user.email


@router.post("auth/password-recovery/{email}", response_model=schemas.Msg)
async def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = cruds.crud_user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = await generate_password_reset_token(uid=user.id)
    send_reset_password_email(
        email_to=user.email, email=user.email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("auth/reset-password/", response_model=schemas.Msg)
async def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    uid = await verify_password_reset_token(token)
    user = cruds.crud_user.get_by_id(db, id=uid)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not cruds.crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}


@router.get("/thtest1")
@throttle.ip_throttle(rate=10, per=60)
async def throttle_test(
        request: Request,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
):
    return "Throttle test endpoint 1 Hello"


@router.get("/thtest2")
@throttle.user_throttle(rate=20, per=60)
async def throttle_test1(
        request: Request,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
):
    return "Throttle test endpoint 2"