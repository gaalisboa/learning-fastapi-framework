from typing import List

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.repositories.postgres.sqlalchemy import get_database
from src.schemas.user_schema import UserSchema, UserCreateSchema
from src.repositories.postgres.user_repository import UserRepository

user_router = APIRouter(prefix='/user')


@user_router.get('/', response_model=List[UserSchema])
def get_all_users(session: Session = Depends(get_database)):
    repository = UserRepository(session)
    users = repository.get_all()
    return users


@user_router.post('/')
def create_user(user: UserCreateSchema, session: Session = Depends(get_database)):
    repository = UserRepository(session)
    user = repository.create(user)
    return user


@user_router.get('/{user_id}', response_model=List[UserSchema])
def get_user_by_id(user_id: int, session: Session = Depends(get_database)):
    repository = UserRepository(session)
    user = repository.get_one(user_id)
    if not user:
        message = {'detail': 'User Not Found'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=message)
    else:
        return user


@user_router.put('/{user_id}', response_model=List[UserSchema])
def update_user(user_id: int, user: UserCreateSchema, session: Session = Depends(get_database)):
    repository = UserRepository(session)
    user = repository.update(user_id, user)
    if not user:
        message = {'detail': 'User Not Found'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=message)
    else:
        return user


@user_router.delete('/{user_id}')
def delete_user(user_id: int, session: Session = Depends(get_database)):
    repository = UserRepository(session)
    deleted = repository.delete(user_id)
    if not deleted:
        message = {'detail': 'User Not Found'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=message)
    else:
        return f'User {deleted.full_name} successfully deleted.'
