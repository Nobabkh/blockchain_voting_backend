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


### End Service import


code_route = APIRouter()

code_paths = [
    '/ws/v2/code/generate'
    
]

'''
main route : /ws/v2/code/
subroutes : [
    /ws/v2/code/generate
    
]


'''





@code_route.websocket("/generate")
async def stream_code(websocket: WebSocket, token: str):
    await websocket.accept()
    print(token)
    # if token != None:
    #     res = populate_from_token(token=token)
    #     if isinstance(res, UserDTO) == False:
    #         await websocket.send_json(
    #             {
    #                 "type": "error",
    #                 "value": "token not valid.",
    #             }
    #         )
    #         return
    # else:
    #     await websocket.send_json(
    #             {
    #                 "type": "error",
    #                 "value": "token not valid.",
    #             }
    #         )
    #     return
    # else:
    #     print('token none')
    #     websocket.close()
    #     return
    # if getuserbyemail(populate_from_token(token=token).email) != None:
    #     print(getuserbyemail(populate_from_token(token=token).email).email)
    
    user = populate_from_token(token=token)
    if user is None:
        await websocket.send_json(
                {
                    "type": "error",
                    "value": "Token Not valid.",
                }
            )
        return
    session = SessionLocal()


    projectid = None
    updatepromt = ''
    pageid = None
    
    projectidjson = await websocket.receive_json()
    if projectidjson['projectid'] != None:
        projectid = projectidjson['projectid']
    pageidjson = await websocket.receive_json()
    if pageidjson['pageid'] != None:
        pageid = pageidjson['pageid']
    # historyidjson = await websocket.receive_json() imurl = savephoto(user=user, image=imdto)
    # if historyidjson['historyid'] != None:
    #     historyid = historyidjson['historyid']
        
    updatepmtjson = await websocket.receive_json()
    if updatepmtjson['updatepromt'] != None:
        updatepromt = updatepmtjson['updatepromt']
    params = await websocket.receive_json()
    
    
    print('received everything')
    
    project = session.query(Project).filter(Project.id == projectid).first()


    # Read the code config settings from the request. Fall back to default if not provided.
    generated_code_config = "html_tailwind"
    
    if project.language != None and project.language != '':
        generated_code_config = project.language
        
    print('retrived project data')

    openai_api_key = os.environ.get("OPENAI_API_KEY")
            # if openai_api_key:
            #     print("Using OpenAI API key from environment variable")

    if not openai_api_key:
        print("OpenAI API key not found")
        await websocket.send_json(
            {
                "type": "error",
                "value": "No OpenAI API key found. Please add your API key in the settings dialog or add it to backend/.env file.",
            }
        )
        return

    # Get the OpenAI Base URL from the request. Fall back to environment variable if not provided.
    openai_base_url = None


    # Get the image generation flag from the request. Fall back to True if not provided.
    should_generate_images = (
        params["isImageGenerationEnabled"]
        if "isImageGenerationEnabled" in params
        else True
    )
    await websocket.send_json({"type": "status", "value": "Generating code..."})

    async def process_chunk(content):
        await websocket.send_json({"type": "chunk", "value": content})

    # Assemble the prompt
    imegestr = params["image"]
    imdto = ImageDTO(img=[imegestr])
    try:
        if params.get("resultImage") and params["resultImage"]:
            prompt_messages = assemble_prompt(
                params["image"], generated_code_config, params["resultImage"]
            )
        else:
            prompt_messages = assemble_prompt(params["image"], generated_code_config)
    except:
        await websocket.send_json(
            {
                "type": "error",
                "value": "Error assembling prompt. Contact support",
            }
        )
        await websocket.close()
        return

    # Image cache for updates so that we don't have to regenerate images
    image_cache = {}
    print('started image cache')
    
    if (params["generationType"] == "update"):
        # Transform into message format
        # TODO: Move this to frontend
        for index, text in enumerate(params["history"]):
            prompt_messages += [
                {"role": "assistant" if index % 2 == 0 else "user", "content": text}
            ]

        image_cache = create_alt_url_mapping(params["history"][-2])
        print('done image cache')

    # if SHOULD_MOCK_AI_RESPONSE:
    #     completion = await mock_completion(process_chunk)
    else:
        if params["generationType"] == "continue":
            await process_chunk(params["history"][0])
    
    print('finally started generating')
            
    completion = await stream_openai_response(
        prompt_messages,
        api_key=openai_api_key,
        callback=lambda x: process_chunk(x),
    )
    print('finally done generating')
        # else:
        #     completion = await stream_openai_response_ncallback(
        #         prompt_messages,
        #         api_key=openai_api_key,
        #         base_url=openai_base_url,
        #     )

    # Write the messages dict into a log so that we can debug later
    # write_logs(prompt_messages, completion)
    #save_Response_for_user(responsetxt=completion, userid=user.id)

    try:
        if should_generate_images:
            # await websocket.send_json(
            #     {"type": "status", "value": "Generating images..."}
            # )
            updated_html = await generate_images(
                completion,
                api_key=openai_api_key,
                base_url=openai_base_url,
                image_cache=image_cache,
            )
        else:
            updated_html = completion
            
        replace1 = 'class=""'
        replace2 = 'style=""'
        updated_html = updated_html.replace(replace1, '')
        updated_html = updated_html.replace(replace2, '')
        
        page = session.query(Page).filter(Page.id == pageid).first()
        page.uri = "/page/"+str(projectid)+"/"+str(pageid)
        session.commit()
        session.flush()
        session.close()
        
        if params["generationType"] == "continue":
            # sitedata = str(params["history"][0]+completion)
            # for st in sitedata.split():
            #     await process_chunk(st)
            updated_html = params["history"][0]+completion
            save_history_v2(userid=user.id, response=updated_html, prompttypeimg=False, pageid=pageid, prompt=updatepromt, promptimg=None)
        elif params["generationType"] == "update":
            # historyid = save_history(userid=user.id, response=updated_html, prompttypeimg=False, prompt=updatepromt, historyid=historyid)
            save_history_v2(userid=user.id, response=updated_html, prompttypeimg=False, pageid=pageid, prompt=updatepromt, promptimg=None)
        elif params["generationType"] == "create":
            imurl = savephoto(user=user, image=imdto)
            #historyid = save_history(userid=user.id, response=updated_html, prompttypeimg=True, promptimg=imurl.url, historyid=historyid)
            save_history_v2(userid=user.id, response=updated_html, prompttypeimg=True, pageid=pageid, prompt=updatepromt, promptimg=imurl.url)

            
            
        tokens = len(updated_html)/4
        tokens = tokens-300
        if tokens >= 600:
            tokens = tokens - 600
            deductToken(uid=user.id)
            if tokens >= 900:
                tokens = int(tokens/900)
                for t in range(tokens):
                    deductToken(uid=user.id)
        await websocket.send_json({"type": "setCode", "value": updated_html})
        await websocket.send_json(
            {"type": "status", "value": "Code generation complete."}
        )
        # await websocket.send_json({"type":"historyid", "value": historyid})
    except Exception as e:
        traceback.print_exc()
        print("Image generation failed", e)
        await websocket.send_json(
            {"type": "status", "value": "Image generation failed but code is complete."}
        )
    finally:
        await websocket.close()


    



@code_route.websocket("/generatesection")
async def section_update(websocket: WebSocket):
    print("got request")
    await websocket.accept()
    # print(token)

    
    # user = populate_from_token(token=token)
    # if user is None:
    #     await websocket.send_json(
    #             {
    #                 "type": "error",
    #                 "value": "Token Not valid.",
    #             }
    #         )
    #     return
    session = SessionLocal()
    # userbalance = session.query(User).filter(User.email == user.email).first()
    # userbalance.addbalance(20.0, datetime.datetime.now() +datetime.timedelta(weeks=4))
    # session.commit()
    # session.flush()
    # session.close()
    # session = SessionLocal()
    # userbalance = session.query(User).filter(User.email == user.email).first()
    # print(userbalance.getbalance())
    # if(userbalance.getbalance() < 2):
    #     await websocket.send_json(
    #             {
    #                 "type": "error",
    #                 "value": "Not enough balance.",
    #             }
    #         )
    #     return
    projectid = None
    updatepromt = ''
    
    projectidjson = await websocket.receive_json()
    if projectidjson['projectid'] != None:
        projectid = projectidjson['projectid']
        
    updatepmtjson = await websocket.receive_json()
    if updatepmtjson['updatepromt'] != None:
        updatepromt = updatepmtjson['updatepromt']
    params = await websocket.receive_json()
    
    project = session.query(Project).filter(Project.id == projectid).first()


    # Read the code config settings from the request. Fall back to default if not provided.
    generated_code_config = "html_tailwind"
    
    if project.language != None and project.language != '':
        generated_code_config = project.language

    openai_api_key = os.environ.get("OPENAI_API_KEY")




    prompt_messages = assemble_prompt_for_section(generated_code_config=generated_code_config, codelist=params, userprompt=updatepromt)



            
    completion = await stream_openai_response_ncallback(prompt_messages, openai_api_key)


    try:

 
        updated_html = completion

        session.commit()
        session.flush()
        session.close()
        

        await websocket.send_json({"type": "setCode", "value": updated_html})

        # await websocket.send_json({"type":"historyid", "value": historyid})
    except Exception as e:
        traceback.print_exc()
        print(e)

    finally:
        await websocket.close()
        
# @code_route.get('/getsection')