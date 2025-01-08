import random
import string
from database.entity.OTP import OTP
from sqlalchemy import TIMESTAMP, desc
import datetime
from database.databaseConfig.databaseConfig import Base, engine, SessionLocal
from dto.UserDTO import UserDTO
from dto.BooleanBasedmessage import BooleanBasedmessage
from database.entity.User import User

def generateotp(userid: int):
    otp =  str(''.join(random.choices(string.ascii_uppercase+string.digits, k=6)))
    session = SessionLocal()
    oserotp = session.query(OTP).filter_by(user_id=userid).order_by(desc(OTP.id)).first()
    if oserotp is None:
        oserotp = OTP(otp=otp, userid=userid)
    else:
        oserotp.otp = otp
        oserotp.generated = datetime.datetime.now()
    
    session.add(oserotp)
    session.flush()
    session.expunge(oserotp)
    session.commit()
    # Close session after committing changes
    session.close()
    return otp

def checkOTPForUser(userid: int, otp: str):
    session = SessionLocal()
    otpForUse = session.query(OTP).filter_by(user_id=userid).order_by(desc(OTP.id)).first()
    if otpForUse is not None:
        print('not none')
        timetogen = otpForUse.generated
        validity_period = datetime.timedelta(minutes=5)  # Adjust this to your desired validity period
        expiry_time = timetogen + validity_period
        timenow = datetime.datetime.now()
        if timenow > expiry_time or otpForUse.otp != otp:
            print('time exp')
            return False
        else:
            user = session.query(User).filter_by(id=userid).first()
            user.user_valid = True
            session.add(user)
            session.commit()
            session.flush()
            session.close()
            return True
    else:
        return False
    
def isOTPIssued(user: UserDTO, otp: str) -> BooleanBasedmessage:
    if checkOTPForUser(userid=user.id, otp=otp):
        return BooleanBasedmessage(state=True, message='Validation Success')
    else:
        return BooleanBasedmessage(state=False, message='OTP not Valid')
    