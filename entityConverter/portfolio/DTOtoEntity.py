from database.entity.User import User
from dto.UserDTO import UserDTO


def user_to_usrdto(user: User):
    return UserDTO(id=user.id,
                   name=user.name,
                   email=user.email,
                   phone=user.phone)