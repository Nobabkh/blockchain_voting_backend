# import os
# import traceback
# from fastapi import APIRouter, WebSocket
# import json
# import asyncio
# ### Start DTO import
# from dto.UserDTO import UserDTO
# from dto.ImageDTO import ImageDTO



# ### End DTO import

# ### Start Service import 

# from service.JWTTokenService import checkToken, populate_from_token
# from template.portfolio.codegen import getallfile, getbackend
# from template.portfolio.automateai import THINKING_CHUNK

# ### End Service import


# template_route = APIRouter()

# template_paths = [
#     '/ws/v2/template/sitejson',
#     '/ws/v2/template/aiquery'
# ]

# '''
# main route : /ws/v2/template/
# subroutes : [
#     /ws/v2/template/sitejson
#     /ws/v2/template/aiquery
# ]


# '''


# @template_route.websocket("/sitejson")
# async def sitejson(websocket: WebSocket, token: str):
    
#     try:
#         user = populate_from_token(token)
#         if isinstance(user, str) == True or checkToken(token) == False:
#             print('invalid user')
#             return
#         await websocket.accept()
#         while True:
#         # async with websocket:
#             data = await websocket.receive_text()
#             jsondata = json.loads(data)
#             async def sendchunk(datas: str):
#                 await websocket.send_json({"process": datas, "state": True})
            
            
            
#             async def sendstatedata(task: str, state: bool):
#                 print({"aistate": {"task": task, "state": state}})
#                 await websocket.send_json({"aistate": {"task": task, "state": state}})
#             async def sendfecode(data: str):
#                 data1 = {"code": data}
#                 await websocket.send_json(data1)    
#             async def sendfile(data: str):
#                 data1 = {"file": data}
#                 await websocket.send_json(data1)      
                
#             async def sendbecode(data: str):
#                 data1 = {"codebe": data}
#                 await websocket.send_json(data1)    
#             async def sendfilebe(data: str):
#                 data1 = {"filebe": data}
#                 await websocket.send_json(data1)                                       
                
            
#             promt = jsondata['promt']+'myname is '+user.username+' email '+user.email+' phone '+user.phone
#             category = ''
#             subcategory = ''
#             tag = ''
#             tempid = -1
#             datastr = ''
#             result = ''
#             template = None
#             # socketdata = await websocket.receive_text()
#             # if socketdata == 'CAT':
#             await websocket.send_json({"aistate": {"task": 'I am scanning your data', "state": False}})
#             # category = await Assemble_CATEGORY(promt)
#             await asyncio.sleep(10)
#             await websocket.send_json({"aistate": {"task": 'I am scanning your data', "state": True}})
#             # print(category)
#             await asyncio.sleep(2)
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'SCAT':
#                 await websocket.send_json({"aistate": {"task": 'I am defining project scope and goals.', "state": False}})
#                 await asyncio.sleep(10)
#                 # await THINKING_CHUNK(sendchunk, jsondata['promt'])
#                 # await websocket.send_json({"process": "", "state": False})  
#                 # subcategory = await ASSEMBLE_SUBCATEGORY(promt, category)

#                 await asyncio.sleep(2)
#                 await websocket.send_json({"aistate": {"task": 'I am defining project scope and goals.', "state": True}})
#                 await asyncio.sleep(1)
#                 # print(subcategory)
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'TAG':
#                 await websocket.send_json({"aistate": {"task": 'I am designing the UI/UX', "state": False}})
#                 await asyncio.sleep(10)
#                 # tag = await ASSEMBLE_TAGLINE(promt, category, subcategory)
#                 await websocket.send_json({"aistate": {"task": 'I am designing the UI/UX', "state": True}})
#                 await websocket.send_json({"aistate": {"task": 'I am generating code for frontend', "state": False}})
#                 # print(tag)
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'TEM':
#                 # tempid = GET_TEMPLATE(subcategory, tag)
#                 # template = TEMPLATESDETAILS[tempid]['JSON'](websocket)
#                 # datastr = await ASSEMBLE_JSON(promt, template.PROMPT)
#                 await getallfile(templatepath='/template1', callback=sendfecode, callbackf=sendfile)
                
#                 await websocket.send_json({"aistate": {"task": 'I am generating code for frontend', "state": True}})
#                 await asyncio.sleep(1)
                    
#                 # print(tempid)g
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'JSON':
#                 await websocket.send_json({"aistate": {"task": 'Linking Assets', "state": False}})
#                 await asyncio.sleep(2)
#                 # result =  await template.LINK(json.loads(datastr))
#                 await websocket.send_json({"sitedata": result}) 
#                 await websocket.send_json({"aistate": {"task": 'Linking Assets', "state": True}})
#                 await asyncio.sleep(1)
                

                
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'SAVE':
#                 await websocket.send_json({"aistate": {"task": 'Done saving', "state": False}})
#                 # session = SessionLocal()
#                 # usersite = UserSitejson(code=json.dumps(result), user_id=user.id, category=category, subcategory=subcategory, tagline=tag, templateid=tempid)
#                 # session.add(usersite)
#                 # session.commit()
#                 # session.flush()
#                 # session.close()
#                 await asyncio.sleep(10)
#                 await websocket.send_json({"aistate": {"task": 'Done saving', "state": True}})
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'PATH':
#                 await websocket.send_json({"aistate": {"task": 'Getting Preview', "state": False}})
#                 # path = TEMPLATESDETAILS[tempid]['HOST']
#                 await websocket.send_json({'PATH': 'path'})
#                 await websocket.send_json({"aistate": {"task": 'Getting Preview', "state": True}})
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'TEST':
#                 await websocket.send_json({"aistate": {"task": 'Testing FrontEnd', "state": False}})
                
#                 socketdata = await websocket.receive_text()
#                 if socketdata == 'TESTDONE':
#                     await websocket.send_json({"aistate": {"task": 'Testing Frontend', "state": True}})
                    
            
#             socketdata = await websocket.receive_text()
#             if socketdata == 'BACKEND':
#                 await websocket.send_json({"aistate": {"task": 'Generating backend logic for connecting functions', "state": False}})
#                 await getbackend('/template1', sendbecode, sendfilebe)
#                 await websocket.send_json({"aistate": {"task": 'Generating backend logic for connecting functions', "state": True}})
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'CONNECT':
#                 await websocket.send_json({"aistate": {"task": 'Connecting frontend and backend', "state": False}})
#                 await asyncio.sleep(5)
#                 await websocket.send_json({"aistate": {"task": 'Connecting frontend and backend', "state": True}})
#                 await websocket.send_json({"CDONE": True})
                
#             socketdata = await websocket.receive_text()
#             if socketdata == 'FITEST':
#                 await websocket.send_json({"aistate": {"task": 'Final test', "state": False}})
#                 await websocket.send_json({"Test": True})
#                 socketdata = await websocket.receive_text()
#                 if socketdata == 'TDONE':
#                     await websocket.send_json({"aistate": {"task": 'Final test', "state": True}})
            
#         #portfolio = portfolioRequest(**json.loads(data))  # Deserialize JSON data into portfolioRequest object
#         #result, category, subcategory, tag, tempid = await getsitejson(jsondata['promt']+'myname is '+user.username+' email '+user.email+' phone '+user.phone, sendstatedata)
        
#         # session = SessionLocal()
#         # usersite = UserSitejson(code=json.dumps(result), user_id=user.id, category=category, subcategory=subcategory, tagline=tag, templateid=tempid)
#         # session.add(usersite)
#         # session.commit()
#         # session.flush()
#         # session.close()
#         # await websocket.send_json({"sitedata": result})  # Serialize result as JSON and send it back
            
#     except Exception as e:
#         print("WebSocket connection closed:", e)
#         await websocket.close()

    

# ### taken  
    
# @template_route.websocket('/aiquery')
# async def strunthinking(websocket: WebSocket):
    
#     try:
#         while True:
#             await websocket.accept()
#             data = await websocket.receive_text()
#             print(data)
#             jsondata = json.loads(data)
#             async def sendchunk(datas: str):
#                 await websocket.send_json({"process": datas, "state": True})
            
#             await THINKING_CHUNK(sendchunk, jsondata['promt'])
#             await websocket.send_json({"process": "", "state": False})  
            
#             # await websocket.send_json({"checklist", ""})
#             await websocket.close()
#             break
#     except Exception as e:
#         print("WebSocket connection closed:", e)
#         await websocket.close()