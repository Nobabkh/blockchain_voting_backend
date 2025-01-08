from enum import Enum

class UserErrorMessages(Enum):
    USERNOTFOUND = 'User Not Found'
    EMAILEXISTS = 'Email Already Exists'
    WRONGPASSWORD = 'Password do not match'
    TOKENEXPIRED = 'Token Expired'
    INVALIDTOKEN = 'Token is not Valid'
    INTERNALERROR = 'BAD Request'
    INVALIDUSER = 'User not valid please contact support'
    EMAILEMPTY = 'Email cannot be empty'
    PASSEMPTY = 'Password cannot be empty'
    PHONEEXIST = 'Phone number already linked to an account'
    LOGGEDINWITHGOOGLE = 'Account is linked with Google use Sign in with Google'