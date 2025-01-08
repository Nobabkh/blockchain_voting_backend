from constant.secret.ApplicationKey import APPLICATION_KEY
from typing import Optional

import jwt
from datetime import datetime, timedelta
from dto.UserDTO import UserDTO
from typing import Union
from database.databaseConfig.databaseConfig import SessionLocal
from database.entity.Token import Token
from sqlalchemy import desc
from database.entity import User

SECRET_KEY = APPLICATION_KEY
expiration_time = datetime.utcnow() + timedelta(hours=24)
expiration_timestamp = int(expiration_time.timestamp())


def create_access_token(user: UserDTO):
    expires_delta = timedelta(minutes=expiration_timestamp)
    to_encode = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "exp": datetime.utcnow() + expires_delta,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt




def populate_from_token(token) -> Union[UserDTO, str]:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = UserDTO(
            id=decoded_token.get("user_id"),
            name=decoded_token.get("name"),
            email=decoded_token.get("email"),
            phone=decoded_token.get('phone'),
        )
        return user
    except jwt.ExpiredSignatureError:
        return 'Token Expired'
    except jwt.InvalidTokenError:
        return 'Invalid Token'
    except Exception as e:
        print(e)
        return str(e)
    
def checkToken(accesstoken: str, temp: Optional[bool] = False) -> bool:
    session = SessionLocal()
    token = session.query(Token).filter_by(access_token=accesstoken).first()
    if token == None:
        return False
    else:
        if temp:
            return True
        else:
            return token.valid


def JWTSecurity(authorization: str, temptoken: Optional[bool] = False):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return False
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        print(user.json())
        print(checkToken(token, temptoken))
        if isinstance(user, UserDTO) and checkToken(token, temptoken):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False