from fastapi import APIRouter, Header, Response
from typing import Union
### Start DTO import
from dto.UserDTOResponse import UserDTOResponse, UserDTOResponseV2
from dto.UserDTO import UserDTO
from dto.HistoryDTO import HistoryDTO
from dto.OnlyPageNumDTO import OnlyPageNumDTO
from dto.HistorypageDTO import HistorypageDTO
from dto.MessageDTO import MessageDTO
from dto.BooleanBasedmessage import BooleanBasedmessage
from dto.WaitlistNumDTO import WaitlistNumDTO
from dto.UserEmailDTO import UserEmailDTO
from dto.ImageDTO import ImageDTO
from dto.ProjectDTO import ProjectDTO, ProjecIDtDTO, DeletePageDTO, ProjectResponseDTO, PageResponseDTO
from dto.ProjectattributeDTO import ProjectattributeDTO
from dto.CodeonlyDTO import CodeIDDTO

### End DTO import

### Start Service import 

# from service.UserService import getuserwithbyemailV2, getuserwithbyemail, total_waitlist
from service.projectService import add_project, add_page_to_project, delete_page, get_all_page, get_all_projects, setprojectattribute, getpageversions, gethistory, get_code_to_render, deleteproject, save_code_history, download_as_zip
from service.JWTTokenService import checkToken, populate_from_token, JWTSecurity
### End Service import

user_path = [
    '/api/v2/user/getuser',
    '/api/v2/user/history'
    
]





project_router_v1 = APIRouter()
project_path_v1 = [
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



    
@project_router_v1.post('/addproject', response_model=BooleanBasedmessage)
def add_new_project(proejct: ProjectDTO, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token)
        if add_project(user=user, project=proejct):
            return BooleanBasedmessage(state=True, message='project added')
        else:
            return BooleanBasedmessage(state=False, message='project adding failed')
    except Exception as e:
        print(e)
        return Response(status_code=403)


@project_router_v1.post('/addpage', response_model=BooleanBasedmessage)
def add_new_page(proejct: ProjecIDtDTO, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if add_page_to_project(user=user, projectid=proejct):
            return BooleanBasedmessage(state=True, message='page added')
        else:
            return BooleanBasedmessage(state=False, message='page adding failed')
    except Exception as e:
        print(e)
        return Response(status_code=403)

    
@project_router_v1.delete('/deletepage', response_model=BooleanBasedmessage)
def delete_page_from_project(proejct: DeletePageDTO, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if delete_page(user=user, project_page=proejct):
            return BooleanBasedmessage(state=True, message='page added')
        else:
            return BooleanBasedmessage(state=False, message='page adding failed')
    except Exception as e:
        print(e)
        return Response(status_code=403)

@project_router_v1.delete('/deleteproject', response_model=BooleanBasedmessage)
def delete_project(project: int, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if deleteproject(project):
            return BooleanBasedmessage(state=True, message='page added')
        else:
            return BooleanBasedmessage(state=False, message='page adding failed')
    except Exception as e:
        print(e)
        return Response(status_code=403)
   

@project_router_v1.get('/getprojects', response_model=list[ProjectResponseDTO])
def add_new_page(authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        return get_all_projects(user)
    except Exception as e:
        print(e)
        return Response(status_code=403)

@project_router_v1.get('/getpages', response_model=list[PageResponseDTO])
def add_new_page(project_id: int, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        return get_all_page(user=user, project_id=project_id)
    except Exception as e:
        print(e)
        return Response(status_code=403)

@project_router_v1.post('/setprojectattr')
def addprojectattribute(projectattr: ProjectattributeDTO, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if setprojectattribute(user=user, project_id=projectattr.project_id, attribute=projectattr.language):
            BooleanBasedmessage(state=True, message='successfull')
    except Exception as e:
        print(e)
        return Response(status_code=403)


@project_router_v1.get('/getpageverison')
def getpversion(pageid: int, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        return getpageversions(user=user, pageid=pageid)
    except Exception as e:
        print(e)
        return Response(status_code=403)


@project_router_v1.get('/gethistory')
def getfullhistory(historyid: int, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        return gethistory(user=user, historyid=historyid)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@project_router_v1.post('/savehistory')
def getfullhistory(codeobj: CodeIDDTO, authorization: str = Header(None)):
    try:
        if JWTSecurity(authorization) == False:
            return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        save_code_history(codeobj)
        return BooleanBasedmessage(state=True, message="Updated")
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@project_router_v1.get('/getcode')
def getcoderender(projectid: int, pageid: int):
    return get_code_to_render(projectid=projectid, pageid=pageid)

@project_router_v1.get('/getzip')
def getzipdownload(projectid: int):
    try:
        # if JWTSecurity(authorization) == False:
        #     return Response(status_code=403)
        # token = authorization.split("Bearer ")[1]
        # user = populate_from_token(token=token)
        
        return download_as_zip(projectid=projectid)
    except Exception as e:
        print(e)
        return Response(status_code=403)



