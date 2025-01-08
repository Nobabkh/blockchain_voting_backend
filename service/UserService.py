from database.databaseConfig.databaseConfig import Base, engine, SessionLocal
from database.entity.User import User
from database.entity.Token import Token
from database.entity.Plan import Plan
from database.entity.Transaction import Transaction
from dto.UserLoginDTO import UserLoginDTO
from dto.UserResponse import UserResponse
from dto.UserError import UserError
from typing import Union, List
from dto.UserDTO import UserDTO, UserProfileDTO
from dto.appenum.UserErrorCodes import UserErrorCodes
from dto.appenum.UserErrorMessages import UserErrorMessages
from service.JWTTokenService import create_access_token, populate_from_token
from service.EmailService import send_OTPBYemail, send_passresetMail, send_waitlistmail
from dto.UserDTOResponse import UserDTOResponseV2, UserDTOResponse
from dto.UserResisterDTO import UserResisterDTO
from sqlalchemy import text
from dto.BooleanBasedmessage import BooleanBasedmessage
from dto.UserpassOTPDTO import UserpassOTPDTO
from service.OTPService import isOTPIssued
from dto.TempTokenRes import TempTokenRes
from dto.GoogleResponseDTO import GoogleResponseDTO
from datetime import datetime
from entityConverter.portfolio.DTOtoEntity import user_to_usrdto
import json
from fastapi import Response

def userLogin(user: UserLoginDTO) -> Union[UserResponse, UserError]:
    session = SessionLocal()
    try:
        tempuser = session.query(User).filter_by(email=user.email).first()

        if user.email is None or user.email == '':
            return UserError(code=UserErrorCodes.EMAILEMPTY.value, message=UserErrorMessages.EMAILEMPTY.value)
        
        if tempuser is not None:
            if tempuser.thirdparty_login:
                return UserError(code=UserErrorCodes.LOGGEDINWITHGOOGLE.value, message=UserErrorMessages.LOGGEDINWITHGOOGLE.value)
        
        if user.password is None or user.password == '':
            return UserError(code=UserErrorCodes.PASSEMPTY.value, message=UserErrorMessages.PASSEMPTY.value)

        userentity = session.query(User).filter_by(email=user.email).first()

        if userentity is not None:
            if userentity.checkPassword(user.password):
                token_data = UserDTO(id=userentity.id, name=userentity.name, email=userentity.email, phone=userentity.phone)
                
                # Fetch or create a token
                token = session.query(Token).filter_by(user_id=userentity.id).first()
                if token is None:
                    token = Token(create_access_token(token_data), userentity.id)
                    session.add(token)
                else:
                    token.access_token = create_access_token(token_data)

                if userentity.user_valid:
                    token.valid = True
                else:
                    token.valid = False

                session.commit()  # Commit all changes before closing the session
                return UserResponse(access_token=token.access_token, validity=token.valid)
            else:
                return UserError(code=UserErrorCodes.WRONGPASSWORD.value, message=UserErrorMessages.WRONGPASSWORD.value)
        else:
            return UserError(code=UserErrorCodes.USERNOTFOUND.value, message=UserErrorMessages.USERNOTFOUND.value)
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(e)
        return UserError(code=UserErrorCodes.INTERNALERROR.value, message=UserErrorMessages.INTERNALERROR.value)
    finally:
        session.close()  # Ensure the session is closed regardless of success or error


   
def userRegister(user: UserResisterDTO) -> Union[UserResponse, UserError]:
    try:
        session = SessionLocal()
        usere = session.query(User).filter_by(email=user.email).first()
            
        if usere is None:
            nuser = User(email=user.email, password=user.password)
            nuser.user_valid = False
            session.add(nuser)
            session.flush()
            session.expunge(nuser)
            token_data = UserDTO(id=nuser.id, name='', email=nuser.email, phone=nuser.phone)
            token = Token(create_access_token(token_data), nuser.id)
            token.valid = False
            session.add(token)
            session.flush()
            session.expunge(token)
            session.commit()
            session.close()
            send_OTPBYemail(nuser.email, "Activate your Account", nuser.id, nuser.email)
            return UserResponse(access_token=token.access_token, validity=False)
        else:
            return UserError(code=UserErrorCodes.EMAILEXISTS.value, message=UserErrorMessages.EMAILEXISTS.value)
    except Exception as e:
        print(e)
        return UserError(code=UserErrorCodes.INTERNALERROR.value, message=UserErrorMessages.INTERNALERROR.value)


def getuserbyemail(email: str):
    try:
        session = SessionLocal()
        user = session.query(User).filter(User.email == email).first()
        return user_to_usrdto(user)
    except Exception as e:
        print(e)
  
    
def getRealuserbyemail(emailr: str) -> Union[User, None]:
    session = SessionLocal()
    result = session.query(User).filter_by(email=emailr).first()
    # user = result
    # session.close()
    print(result == None)
    if result is None:
        return None
    else:
        result


def deductToken(uid: int):
    session = SessionLocal()
    user = session.query(User).filter_by(id=uid).first()
    if user is not None:
        user.useToken()
        session.commit()
        session.close()
        
def resetpass(email: str) -> BooleanBasedmessage:
    user = getuserbyemail(email=email)
    if send_passresetMail(email, 'Reset your password', user.id):
        return BooleanBasedmessage(state=True, message='OTP sent Successfully')
    else:
        return BooleanBasedmessage(state=False, message='Something went wrong')
    
def checkresetpassotp(userotp: UserpassOTPDTO) -> Union[TempTokenRes, BooleanBasedmessage]:
    try:
        user = getuserbyemail(email=userotp.email)
        print(user)
        res = isOTPIssued(user=user, otp=userotp.otp)
        print(res)
        if(res.state):
            session = SessionLocal()
            token = Token(create_access_token(user=user), user.id)
            token.valid = False
            tokenstr = token.access_token
            session.add(token)
            session.commit()
            session.flush()
            session.close()
            return TempTokenRes(access_token=tokenstr, temp=True)
        else:
            return res
    except Exception as e:
        print(e)
    
def changepass(user:UserDTO, password: str):
    try:
        session = SessionLocal()
        usern = session.query(User).filter_by(email=user.email).first()
        usertemp = User(email=user.email, password=password)
        usern.password = usertemp.password
        session.commit()
        session.flush()
        return BooleanBasedmessage(state=True, message='password changed successfully')
    except Exception as e:
        return BooleanBasedmessage(state=False, message='password changed failed')
    
def signinwithGoogle(guser: GoogleResponseDTO):
    try:
        session = SessionLocal()
        exuser = session.query(User).filter_by(email=guser.email).first()
        
        if exuser is None:
            nuser = User(email=guser.email, thirdparty_login=True, thirdparty_name='GOOGLE')
            nuser.name = guser.name
            session.add(nuser)
            session.commit()
            session.flush()
            dbuser = session.query(User).filter_by(email=nuser.email).first()
            token_user = user_to_usrdto(dbuser)
            token = session.query(Token).filter_by(user_id=dbuser.id).first()
            if token == None:
                token = Token(create_access_token(token_user), dbuser.id)
                session.add(token)
            else:
                token.access_token = create_access_token(token_user)
                
            session.commit()
            session.flush()
            return UserResponse(access_token=token.access_token, validity=True)
            
        else:
            dbuser = session.query(User).filter_by(email=guser.email).first()
            token_user = user_to_usrdto(user=dbuser)
            token = Token(create_access_token(token_user), dbuser.id)
            session.add(token)
            session.commit()
            session.flush()
            return UserResponse(access_token=token.access_token, validity=True)
        
    except Exception as e:
        print(e)
        return UserError(code=UserErrorCodes.INTERNALERROR.value, message=UserErrorMessages.INTERNALERROR.value)
    
def userlogout(userid: int) -> BooleanBasedmessage:
    try:
        session = SessionLocal()
        session.query(Token).filter_by(user_id=userid).delete()
        session.commit()
        session.close()
        return BooleanBasedmessage(state=True, message='Logout successfull')
    except Exception as e:
        return BooleanBasedmessage(state=False, message='Try again')
    
    
def updateuser(userprofile: UserProfileDTO) -> BooleanBasedmessage:
    try:
        session = SessionLocal()
        user = session.query(User).filter(User.id == userprofile.id).first()
        if userprofile.name:
            user.name = userprofile.name
        if userprofile.gender:
            user.gender = userprofile.gender
        if userprofile.phone:
            user.phone = userprofile.phone
        if userprofile.bio:
            user.bio = userprofile.bio
        if userprofile.country:
            user.country = userprofile.country
        session.commit()
        session.flush()
        session.close()
        return BooleanBasedmessage(state=True, message='account updated')
    except Exception as e:
        return BooleanBasedmessage(state=False, message='failed to update')
    

def getuserprofile(user: UserDTO):
    try:
        session = SessionLocal()
        userdb = session.query(User).filter(User.id == user.id).first()
        return UserProfileDTO(id=userdb.id, name=userdb.name, phone=userdb.phone, email=userdb.email, gender=userdb.gender, bio=userdb.bio, country=userdb.country)
    except Exception as e:
        return Response(status_code=403)
        
    

    
