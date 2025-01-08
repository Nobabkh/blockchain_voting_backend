from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRouter
from collections import defaultdict
import time


class RateLimiter:
    def __init__(self, app: FastAPI, limit: int = 2, interval: int = 60, block_duration: int = 300):
        self.app = app
        self.limit = limit
        self.interval = interval
        self.block_duration = block_duration
        self.blocked_ips = defaultdict(int)

    def middleware(self, request: Request):
        client_ip = request.client.host
        print('inside')
        if self.blocked_ips != None:
            print(self.blocked_ips[client_ip])

        # Check if the IP is blocked
        if self.blocked_ips[client_ip] > time.time():
            print('ip blocked')
            raise HTTPException(status_code=403, detail="IP blocked")

        # Increment the request count for the IP
        self.blocked_ips[client_ip] += 1

        # Remove IPs from the blocked list if their block duration has expired
        self.blocked_ips = {ip: block_time for ip, block_time in self.blocked_ips.items() if block_time > time.time()}

        # Check if the IP has exceeded the rate limit
        if self.blocked_ips[client_ip] > self.limit:
            # Block the IP for the specified duration
            self.blocked_ips[client_ip] = time.time() + self.block_duration
            print('ip blocked')
            raise HTTPException(status_code=403, detail="IP blocked")
        
        return

