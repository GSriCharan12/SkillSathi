"""
SkillSathi - Authentication API Router
Handles User Registration, Family Room Joining, and JWT Token Issuance.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.family import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserRead,
)
from app.services.family_service import FamilyService
from app.security.auth import get_current_user
from app.models.family import User
from app.utils.response import success_response

router = APIRouter(prefix="/auth", tags=["Authentication & Access Control"])


@router.post(
    "/register",
    response_model=ApiResponse[TokenResponse],
    summary="Register new user & create/join family room",
    description="Registers a learner or parent, assigns a unique family code (e.g. SK-4921) or joins an existing room, and issues a JWT token."
)
async def register(
    req: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    user, token, family_code = FamilyService.register_user(db=db, req=req)
    token_data = TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserRead.model_validate(user),
        family_code=family_code,
        family_id=user.family_id
    )
    return success_response(
        data=token_data.model_dump(),
        message="User registered and family room assigned successfully."
    )


@router.post(
    "/login",
    response_model=ApiResponse[TokenResponse],
    summary="Authenticate user and issue session token",
    description="Authenticates with email/phone and password, returning user profile and family session info."
)
async def login(
    req: UserLoginRequest,
    db: Session = Depends(get_db)
):
    user, token, family_code = FamilyService.authenticate_user(db=db, req=req)
    token_data = TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserRead.model_validate(user),
        family_code=family_code,
        family_id=user.family_id
    )
    return success_response(
        data=token_data.model_dump(),
        message="Authentication successful."
    )


@router.get(
    "/me",
    response_model=ApiResponse[UserRead],
    summary="Get current authenticated user profile",
    description="Returns current authenticated user details, assigned role, and family association."
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return success_response(
        data=UserRead.model_validate(current_user).model_dump(),
        message="User profile retrieved."
    )


@router.post(
    "/logout",
    response_model=ApiResponse[None],
    summary="Logout user session",
    description="Invalidates current frontend session."
)
async def logout(
    current_user: User = Depends(get_current_user)
):
    return success_response(
        data=None,
        message="Session successfully terminated."
    )
