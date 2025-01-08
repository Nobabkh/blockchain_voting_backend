import base64
from fastapi import APIRouter, Header, Response
from typing import Union

### Start DTO import
from dto.OnlyUrlDTO import OnlyUrlDTO
from dto.ImageDTO import ImageDTO
from dto.BooleanBasedmessage import BooleanBasedmessage

### End DTO import


### Start Service import 

from service.JWTTokenService import checkToken, populate_from_token
from sshort import take_full_page_screenshot, take_full_page_screenshot_ao

### End Service import

screenshoot_router = APIRouter()

screenshot_path = [
    '/api/v2/screenshot/fullpage',
    '/api/v2/screenshot/chunk'
]

'''
main route : /api/v1/screenshot
subroutes : [
    /api/v2/screenshot/fullpage,
    /api/v2/screenshot/chunk
]


'''


def bytes_to_data_url(image_bytes: bytes, mime_type: str) -> str:
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{base64_image}"

@screenshoot_router.post('/fullpage', response_model=Union[ImageDTO, BooleanBasedmessage])
def screenshort(url: OnlyUrlDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
            print('token false')
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        
        image = take_full_page_screenshot_ao(url=url.url)
        if isinstance(image, BooleanBasedmessage):
            return image
        else:
            return ImageDTO(img=image)
    except Exception as e:
        print(e)
        return BooleanBasedmessage(state=True, message='Invalid Url')
    
@screenshoot_router.post('/chunk', response_model=Union[ImageDTO, BooleanBasedmessage])
def screenshortv2(url: OnlyUrlDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        
        image = take_full_page_screenshot(url=url.url)
        return ImageDTO(img=image)
    except Exception as e:
        print(e)
        return BooleanBasedmessage(state=True, message='Invalid Url')

