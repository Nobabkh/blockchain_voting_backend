import os
import traceback
from fastapi import APIRouter, HTTPException, WebSocket
### Start DTO import
from dto.UserDTO import UserDTO
from dto.ImageDTO import ImageDTO

import datetime



### End DTO import

from database.entity.User import User
from database.databaseConfig.databaseConfig import SessionLocal
from database.entity.Project import Project
from database.entity.Page import Page
from database.entity.History import History

### Start Service import 

from service.JWTTokenService import checkToken, populate_from_token
from service.UserService import getuserbyemail, deductToken, getRealuserbyemail
from prompts import assemble_prompt
from sectionPrompts import assemble_prompt_for_section
from image_generation import create_alt_url_mapping
from llm import stream_openai_response, stream_openai_response_ncallback
from service.ImageStorage import savephoto
from service.ResponseService import save_history, save_history_v2
from image_generation import create_alt_url_mapping, generate_image, generate_images
from service.code_generation_service import generate_code_stream, chat_stream
from sshort import take_full_page_screenshot_ao

### End Service import


core_route = APIRouter()

code_paths = [
    '/ws/v2/code/generate'
    
]

'''
main route : /ws/v2/code/
subroutes : [
    /ws/v2/code/generate
    
]


'''


'''
receiving JSON structre
{
    prompt: str,
    imagebytes: str | None,
    weburl: str | None,
    exit: bool
    
}
'''




@core_route.websocket("/generate")
async def stream_code(websocket: WebSocket):
    try:
        await websocket.accept()
        
        while True:
            user_prompt = await websocket.receive_json()
            print(user_prompt)
            
            # if user_prompt['exit'] == True:
            #     return
            
            if user_prompt['imagebytes'] is not None:
                await generate_code_stream(websocket=websocket, prompt=user_prompt['prompt'], imagebyte=user_prompt['imagebytes'])
            elif user_prompt['weburl'] is not None:
                await generate_code_stream(websocket=websocket, prompt=user_prompt["prompt"], imagebyte=take_full_page_screenshot_ao(user_prompt['weburl']))
            else:
                await chat_stream(websocket=websocket, prompt=user_prompt['prompt'])
        
    except Exception as e:
        print(e)

    finally:
        await websocket.close()
