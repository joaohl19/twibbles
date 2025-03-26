from model.pydantic.user import CreateUser
from model.pydantic.user import User as UserPydantic
from model.sqlalchemy.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.engine import postgresql_engine
from src.schemas.response import HttpResponseModel


def get_user(user_id: int):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.id == user_id).limit(1)
            user = session.execute(statement).scalars().first()

            if user is None:
                return HttpResponseModel(status_code=404, message="User not found")

            user = UserPydantic(id=user.id,
                                user_name=user.user_name,
                                email=user.email,
                                is_private=user.is_private,
                                profile_img_path=user.profile_img_path,
                                bio=user.bio,
                                ).model_dump()

            return HttpResponseModel(status_code=200,
                                     message="User found",
                                     data=user)
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))

def get_users_by_substring(substring: str):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.user_name.ilike(f"%{substring}%"))
            users = session.execute(statement).scalars().all()

            users = [UserPydantic(id=user.id,
                                  user_name=user.user_name,
                                  profile_img_path=user.profile_img_path,
                                  ).model_dump() for user in users]

            return HttpResponseModel(status_code=200,
                                     message="Users found",
                                     data=users)
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))


def update_user_privacy(user_id: int, is_private: bool):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.id == user_id).limit(1)
            user = session.execute(statement).scalars().first()

            if user is None:
                return HttpResponseModel(status_code=404, message="User not found")
            
            user.is_private = is_private
            session.commit()

            return HttpResponseModel(status_code=200,
                                        message="User privacy updated")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))


def delete_user(user_id: int):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.id == user_id).limit(1)
            user = session.execute(statement).scalars().first()

            if user is None:
                return HttpResponseModel(status_code=404, message="User not found")

            session.delete(user)
            session.commit()

            return HttpResponseModel(status_code=200,
                                     message="User deleted")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))


def create_user(user_data: CreateUser):
    try:
        with Session(postgresql_engine) as session:
            user = User(user_name=user_data.user_name,
                        email=user_data.email,
                        password=user_data.password,
                        is_private=user_data.is_private,
                        profile_img_path=user_data.profile_img_path,
                        bio=user_data.bio)
            session.add(user)
            session.commit()

            return HttpResponseModel(status_code=201,
                                     message="User created")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))
    
def update_password(user_id: int, password: str):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.id == user_id).limit(1)
            user = session.execute(statement).scalars().first()

            if user is None:
                return HttpResponseModel(status_code=404, message="User not found")

            user.password = password
            session.commit()

            return HttpResponseModel(status_code=200,
                                        message="User privacy updated")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))
    
def update_profile(user_id: int, user_name: str, profile_img_path: str, bio: str):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.id == user_id).limit(1)
            user = session.execute(statement).scalars().first()

            if user is None:
                return HttpResponseModel(status_code=404, message="User not found")

            user.user_name = user_name
            user.user_name = profile_img_path
            user.user_name = bio
            session.commit()

            return HttpResponseModel(status_code=200,
                                        message="User privacy updated")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))