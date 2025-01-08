from fastapi import APIRouter, Header, Response, HTTPException
from typing import Union
import requests
### Start DTO import
from dto.UserLoginDTO import UserLoginDTO
from dto.UserResponse import UserResponse
from dto.UserError import UserError
from dto.BooleanBasedmessage import BooleanBasedmessage
from dto.TempTokenRes import TempTokenRes
from dto.OnlyemailDTO import OnlyemailDTO
from dto.UserpassOTPDTO import UserpassOTPDTO
from dto.OnlyPassDTO import OnlyPassDTO
from dto.UserResisterDTO import UserResisterDTO
from dto.UserDTO import UserDTO, UserProfileDTO
from dto.OTPDTO import OTPDTO
from dto.GoogleResponseDTO import GoogleResponseDTO
from dto.CodeonlyDTO import CodeonlyDTO
from pydantic import BaseModel

### End DTO import

### Start Service import 

from service.UserService import userLogin, resetpass, checkresetpassotp, changepass, userRegister, isOTPIssued, signinwithGoogle, userlogout, updateuser
from service.JWTTokenService import checkToken, populate_from_token
from service.EmailService import send_OTPBYemail

### End Service import

auth_paths = [
    '/api/v2/auth/login',
    '/api/v2/auth/resetpass',
    '/api/v2/auth/confirmresetpass',
    '/api/v2/auth/changepass',
    '/api/v2/auth/user',
    '/api/v2/auth/waituser',
    '/api/v2/auth/user/otp',
    '/api/v2/auth/user/reendotp',
    '/api/v2/auth/google',
    '/api/v2/auth/logout'
    
]
auth_router = APIRouter()

'''
main route : /api/v2/auth
subroutes : [
    /api/v2/auth/login,
    /api/v2/auth/resetpass,
    /api/v2/auth/confirmresetpass,
    /api/v2/auth/changepass,
    /api/v2/auth/user,
    /api/v2/auth/waituser,
    /api/v2/auth/user/otp,
    /api/v2/auth/user/reendotp,
    /api/v2/auth/google,
    /api/v2/auth/logout
    
]


'''





@auth_router.post(path='/login', response_model=Union[UserResponse, UserError])
def Login(user: UserLoginDTO):
    return userLogin(user=user)

@auth_router.post(path='/resetpass', response_model=BooleanBasedmessage)
def reset_pass(user: OnlyemailDTO):
    return resetpass(user.email)
    
@auth_router.post(path='/confirmresetpass', response_model=Union[BooleanBasedmessage, TempTokenRes])
def reset_pass(userotp: UserpassOTPDTO):
    return checkresetpassotp(userotp=userotp)

@auth_router.post(path='/changepass', response_model=BooleanBasedmessage)
def user_changepass(userp: OnlyPassDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, UserDTO) and checkToken(token, temp=True):
            return changepass(user, userp.password)
        else:
            return Response(status_code=403)
    except Exception as e:
        print(e)
        return Response(status_code=403)


@auth_router.post(path='/user', response_model=Union[UserResponse, UserError])
def Register(user: UserResisterDTO):
    return userRegister(user=user)

@auth_router.post(path='/user/otp', response_model=BooleanBasedmessage)
def checkOTP(otp: OTPDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, UserDTO) and checkToken(token, True):
            return isOTPIssued(user=user, otp=otp.otpCode)
        else:
            return Response(status_code=403)
    except Exception as e:
        print(e)
        return Response(status_code=403) 
    
    
@auth_router.post(path='/user/resendotp')
def resendOTP(authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]

        user = populate_from_token(token=token)
        if isinstance(user, UserDTO) and user != None and checkToken(token, True):
            send_OTPBYemail(recipient_email=user.email, subject='Activate your Account', userid=user.id, username=user.name)
            return BooleanBasedmessage(state=True, message='Resend OTP successful')
        else:
            return Response(status_code=403)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@auth_router.post("/google")
async def auth_google(code: CodeonlyDTO):
    url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {
        "Authorization": "Bearer " + code.code,
        'Access-Control-Allow-Origin': 'http://genwebbuilder.com',
        'Access-Control-Allow-Credentials': 'true'
    }

    try:
        response = requests.get(url, headers=headers, cookies={"withCredentials": "true"})
        response.raise_for_status() 
        print(response)
        print('api response')
        
        print(response.json())
        gres = GoogleResponseDTO(id=response.json()['id'], email=response.json()['email'], verified_email=response.json()['verified_email'], name=response.json()['name'], given_name=response.json()['given_name'], family_name=response.json()['family_name'], picture=response.json()['picture'], locale='None')
        print(gres.email)
        return signinwithGoogle(gres)
        # return UserResponse(access_token='', validity=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Request to Google API failed") from e

@auth_router.post('/logout', response_model=BooleanBasedmessage)
def logout(authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        return userlogout(user.id)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@auth_router.post('/update', response_model=BooleanBasedmessage)
def update_user(userupdate: UserProfileDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, UserDTO):
            return updateuser(userprofile=userupdate)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
    
GITHUB_CLIENT_ID = "YOUR_GITHUB_CLIENT_ID"
GITHUB_CLIENT_SECRET = "YOUR_GITHUB_CLIENT_SECRET"
GITHUB_OAUTH_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API = "https://api.github.com/user"


class GitHubOAuthResponse(BaseModel):
    access_token: str
    token_type: str


@auth_router.get("/auth/github/callback")
async def github_callback(code: str):
    # Exchange the code for an access token
    response = requests.post(
        GITHUB_OAUTH_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch access token")

    token_data = response.json()
    access_token = token_data.get("access_token")

    # Fetch user information
    user_response = requests.get(
        GITHUB_USER_API,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if user_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user information")

    user_data = user_response.json()
    print(user_response.json())
    return {"user": user_data}