from fastapi import APIRouter, Header, Response
from typing import Union
### Start DTO import
from dto.UserDTOResponse import UserDTOResponse, UserDTOResponseV2
from dto.UserDTO import UserDTO, UserProfileDTO
from dto.HistoryDTO import HistoryDTO
from dto.OnlyPageNumDTO import OnlyPageNumDTO
from dto.HistorypageDTO import HistorypageDTO
from dto.MessageDTO import MessageDTO
from dto.BooleanBasedmessage import BooleanBasedmessage
from dto.WaitlistNumDTO import WaitlistNumDTO
from dto.UserEmailDTO import UserEmailDTO
from dto.ImageDTO import ImageDTO

### End DTO import

### Start Service import 

# from service.UserService import getuserwithbyemailV2, getuserwithbyemail, total_waitlist
from service.JWTTokenService import checkToken, populate_from_token
from service.HistoryService import gethistorylist, getcurrenthistory, getdetailedhistory
from service.EmailService import send_Email, send_user_Email
from service.ImageStorage import savephoto
from service.UserService import getuserprofile

### End Service import

user_path = [
    '/api/v2/user/getuser',
    '/api/v2/user/history'
    
]





user_router_v1 = APIRouter()
user_path_v1 = [
    '/api/v1/user/getuser',
    '/api/v1/user/history',
    '/api/v1/user/sendmessage',
    '/api/v1/user/all',
    '/api/v1/user/sendmail',
    '/api/v1/user/savephoto',
    '/api/v1/user/historylist',
    '/api/v1/user/curhistory',
    '/api/v1/user/getdthistory'
    
]

'''
main route : /api/v1/user
subroutes : [
    /api/v1/user/getuser,
    /api/v1/user/history,
    /api/v1/user/sendmessage,
    /api/v1/user/all,
    /api/v1/user/sendmail,
    /api/v1/user/savephoto,
    /api/v1/user/historylist,
    /api/v1/user/curhistory,
    /api/v1/user/getdthistory
    
]


'''

    
@user_router_v1.get(path='/getUser', response_model=Union[UserProfileDTO, None])
def getuserDetails(authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)

        
        return getuserprofile(user)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    


@user_router_v1.post('/sendmessage')
def send_message(mail: MessageDTO):
    try:
        if send_Email(requestmail=mail.uemail, name=mail.name, message=mail.message):
            return BooleanBasedmessage(state=True, message='Message sent successfully')
        else:
            return BooleanBasedmessage(state=False, message='Something went wrong')
    except Exception as e:
        print(e)
        return BooleanBasedmessage(state=False, message='Something went wrong')
    

@user_router_v1.post('/sendmail')
def sendusermail(um: UserEmailDTO):
    if send_user_Email(requestmail=um.requesemail, subject=um.subject, message=um.message, usermail=um.fromuser):
        return BooleanBasedmessage(state=True, message='message sent')
    else:
        return BooleanBasedmessage(state=True, message='message sent failed')
    
@user_router_v1.post('/savephoto')
def paymentcheck(image: ImageDTO ,authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
            print('header')
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            print('fault token 1')
            return Response(status_code=403)
        if user == None:
            print('fault token 2')
            return Response(status_code=403)
        # print(user.id)
        return savephoto(user=user, image=image)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@user_router_v1.get('/historylist')
def gethistorylistapi(authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
            print('header')
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        if user == None:
            return Response(status_code=403)
        # print(user.id)
        return gethistorylist(userid=user.id)
    except Exception as e:
        print(e)
        return Response(status_code=403)
        
        
@user_router_v1.get('/curhistory')
def getcurhistoryapi(authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
            print('header')
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        if user == None:
            return Response(status_code=403)
        # print(user.id)
        return getcurrenthistory(userid=user.id)
    except Exception as e:
        print(e)
        return Response(status_code=403) 
    
@user_router_v1.post('/getdthistory')
def getdthistory(id: OnlyPageNumDTO):
    return getdetailedhistory(historyid=id.page)
    









