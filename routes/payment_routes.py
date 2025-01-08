from fastapi import APIRouter, Header, Response, requests, HTTPException, Request
from ip2geotools.databases.noncommercial import DbIpCity
### Start DTO import
from dto.PaymmentRequestDTO import PaymentRequestDTO, PAGRequestDTO
from dto.BooleanBasedmessage import BooleanBasedmessage
from dto.CouponPlanDTO import CouponPlanDTO



### End DTO import

### Start Service import 

from service.JWTTokenService import checkToken, populate_from_token
from service.PaymentService import gettpayment_url, initializestripe, checktcoupon, checkpayment, updatepay, payasyougolink, stpayasyougo
from service.Planservice import getallplans

### End Service import


payment_route = APIRouter()
payment_paths = [
    '/api/v2/payment/sslcmz/payurl',
    '/api/v2/payment/stripe/init',
    '/api/v2/payment/applytoken',
    '/api/v2/payment/sslcmz/checkpayment',
    '/api/v2/payment/stripe/update',
    '/api/v2/payment/sslcmz/payasgolink',
    '/api/v2/payment/stripe/initpayasgo',
    '/api/v2/payment/getallplans',
    
]

'''
main route : /api/v2/payment/
subroutes : [
    /api/v2/payment/sslcmz/payurl,
    /api/v2/payment/stripe/init,
    /api/v2/payment/applytoken,
    /api/v2/payment/sslcmz/checkpayment,
    /api/v2/payment/stripe/update,
    /api/v2/payment/sslcmz/payasgolink,
    /api/v2/payment/stripe/initpayasgo,
    /api/v2/payment/getallplans,
    
    
    
]


'''


@payment_route.post('/sslcmz/payurl')
def getpay_url(pay: PaymentRequestDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        return gettpayment_url(userid=user.id, planid=pay.plan_id, amount=pay.amount, address=pay.address, country=pay.country, city=pay.city, token=token, ccode=pay.ccode, coupon=pay.coupon)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@payment_route.post('/stripe/init')
def getpay_url(pay: PaymentRequestDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        return initializestripe(userid=user.id, planid=pay.plan_id, amount=pay.amount, coupon=pay.coupon)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@payment_route.post('/applytoken')
def applitoken(coupon: CouponPlanDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            print('token not found')
            return Response(status_code=403)
        else:
            return checktcoupon(coupon, user.id)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    

@payment_route.post('/sslcmz/checkpayment')
def paymentcheck(authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        # print(user.id)
        return checkpayment(user.id)
    except Exception as e:
        print(e)
        return Response(status_code=403)
@payment_route.post('/stripe/update')
def paymentcheck(authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        # print(user.id)
        return updatepay(user.id)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@payment_route.post('/sslcmz/payasgolink')
def payasgo(pag: PAGRequestDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        # print(user.id)
        return payasyougolink(pay=pag, userid=user.id, token=token)
    except Exception as e:
        print(e)
        return Response(status_code=403)
    
@payment_route.post('/stripe/initpayasgo')
def payasgo(pag: PAGRequestDTO, authorization: str = Header(None)):
    try:
        if authorization is None or not authorization.startswith("Bearer "):
                return Response(status_code=403)
        token = authorization.split("Bearer ")[1]
        user = populate_from_token(token=token)
        if isinstance(user, str) or checkToken(token) == False:
            return Response(status_code=403)
        # print(user.id)
        return stpayasyougo(pag, user.id)
    except Exception as e:
        print(e)
        return Response(status_code=403)
@payment_route.get('/getallplans')
async def getallplan(request: Request):
    try:
        client_ip = request.client.host.split(":")[0]
        response = DbIpCity.get(client_ip, api_key='free')
        
        if response is None:
            raise HTTPException(status_code=402, detail="Failed to retrieve location data")

        country = response.country
        print(country)
        return getallplans(country)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    



