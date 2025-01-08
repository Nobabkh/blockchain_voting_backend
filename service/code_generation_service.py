import os
import traceback
from fastapi import APIRouter, WebSocket
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



async def generate_code_stream(websocket: WebSocket, prompt: str, imagebyte: str):
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    async def process_chunk(content):
        await websocket.send_json({"type": "chunk", "value": content})

    user_content = [
    {
        "type": "image_url",
        "image_url": {"url": imagebyte, "detail": "high"},
    },
    {
        "type": "text",
        "text": prompt,
    },]
    system_content = [
    {
        "type": "text",
        "text": (
            "You are an expert web developer developer."
            "Please keep close attention to detail on given image and generate react ts tailwind code if the user does not specify any technology."
            "Your output should be in markdown format."
        ),
    },
    ]
    prompt_message =  [
    {
        "role": "system",
        "content": system_content,
    },
    {
        "role": "user",
        "content": user_content,
    },
    ]


            
    await stream_openai_response(
        prompt_message,
        api_key=openai_api_key,
        callback=lambda x: process_chunk(x),
    )



async def chat_stream(websocket: WebSocket, prompt: str):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    await websocket.send_json({"type": "status", "value": "Generating code..."})

    async def process_chunk(content):
        await websocket.send_json({"type": "chunk", "value": content})

    user_content = [
        {
            "type": "text",
            "text": prompt,
        },
    ]
    system_content = [
        {
            "type": "text",
            "text": (
                "You are an expert web developer named Websparks, developed by Contessa."
                "When generating code, always include the filename beside the code format type in the following format: ```tsx Filename.tsx."
                "Do not put the filename on a new line. sctricly follow format without newline ```tsx pagename.tsx "
                "Ensure the filename is directly next to the code type within the same code block header."
                "If the user does not specify a technology, use React with TypeScript and Tailwind CSS as defaults."
            ),
        },
    ]

    prompt_message = [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]

    await stream_openai_response(
        prompt_message,
        api_key=openai_api_key,
        callback=lambda x: process_chunk(x),
    )
