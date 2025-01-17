from enum import Enum

class DocumentStateEnum(Enum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    EXPIRED = 4
    ONHOLD = 5
    NEEDS_CHANGES = 6
    DRAFT_NEEDS_SIGNERS = 7
    DRAFT_NEEDS_SIGNER_POS = 8
    
    
class SignerWorkTypeENUM(Enum):
    SIGN = 1
    APPROVE = 2

    
def convert_enum_value_to_string(enum_value: int) -> str:
    try:
        # Convert the integer to the corresponding DocumentStateEnum
        return DocumentStateEnum(enum_value).name
    except ValueError:
        # If the integer does not match any enum, return an appropriate message
        return "Invalid enum value"
