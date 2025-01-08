# Load environment variables first
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime
import time
import json
import os

# Fastapi imports
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.openapi.utils import get_openapi
# from database.entity.User import User

# end Fastapi import 

from routes.auth_routes import auth_router
from routes.code_generator_routes import code_route
from routes.user_routes import user_router_v1
from routes.screenshot import screenshoot_router
from routes.project_routes import project_router_v1
from routes.payment_routes import payment_route
from routes.core_routes import core_route

# load .env
load_dotenv()

# database migrate and seed
# from database.databaseConfig.migrate import Migrate

# services






max_requests_per_minute = 60
block_duration = 300  # 5 minutes



secutity = HTTPBearer()



# seed_all()              
    
app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)



class IPSecurity:
    ip: str
    req_count: int
    blocked: bool
    blocked_time: datetime
    
    def __init__(self, ip: str):
        self.ip = ip

ip_counts = {}




origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:80",
    "http://localhost",
    "http://10.10.50.11",
    "http://websparks.ai",
    "https://websparks.ai"
    # Add more origins as needed, comma-separated
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)




# app.include_router(router=auth_router, prefix='/api/v1/auth')
# app.include_router(router=user_router_v1, prefix='/api/v1/user')
# app.include_router(router=project_router_v1, prefix='/api/v1/project')
# app.include_router(router=code_route, prefix='/ws/code')
# app.include_router(router=screenshoot_router, prefix='/api/v1/screenshot')
# app.include_router(router=payment_route, prefix='/api/v1/payment')

app.include_router(router=core_route, prefix='/ws/core')


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="websparks",
        version="2.0",
        description="API DOcumentation for websparks Backend",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi 
    

if __name__ == "__main__":
    import uvicorn
    # import ssl

    # certfile = '/var/projects/openssl/websparks.ai.pem'
    # keyfile = '/var/projects/openssl/websparks.ai.key'
    # cafile = '/var/projects/openssl/cloudflare-rsa-chain.pem'

    # Run the FastAPI app with Uvicorn using SSL
    # Migrate()
    # uvicorn.run(
    #     app,
    #     host="0.0.0.0",
    #     port=7001,
    #     ssl_certfile=certfile,
    #     ssl_keyfile=keyfile,
    #     ssl_ca_certs=cafile
    # )

    uvicorn.run(app, host="0.0.0.0", port=7001)
    # uvicorn.run(app, host="0.0.0.0", port=7001, ssl_certfile=alternate, ssl_keyfile=alternate)


