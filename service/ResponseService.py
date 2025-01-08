from database.databaseConfig.databaseConfig import SessionLocal
from database.entity.History import History, HistoryList
from sqlalchemy import desc
from datetime import datetime
from database.entity.Page import Page

        
def save_history(userid: int, response: str, prompttypeimg: bool,pageid: int, prompt: str = None, promptimg: str = None, historyid: int = None) -> int:
    try:
        historyidf = 0
        session = SessionLocal()
        history = History(response=response, user_id=userid, prompttypeimage=prompttypeimg, promt=prompt, promptimg=promptimg)
        history.page_id = pageid
        historylist = None
        if historyid != None:
            historylist = session.query(HistoryList).filter_by(id=historyid).order_by(desc(HistoryList.id)).first()
            history.history_list = historylist
            historyidf = historylist.id
        else:
            historylist = HistoryList(datetime.now(), user_id=userid)
            session.add(historylist)
            history.history_list = historylist
            
        session.add(history)
        session.commit()
        session.flush()
        historyidf = historylist.id
        return historyidf
    except Exception as e:
        print(e)
        
        
def save_history_v2(userid: int, response: str, prompttypeimg: bool,pageid: int, prompt: str = None, promptimg: str = None):
    try:
        session = SessionLocal()
        history = History(response=response, user_id=userid, prompttypeimage=prompttypeimg, promt=prompt, promptimg=promptimg)
        history.page_id = pageid
            
        session.add(history)
        session.commit()
        session.flush()
        session.close()
    except Exception as e:
        print(e)
# def update_history(userid: int, response: str, historyid: int):
#     try:
#         session = SessionLocal()
#         history = session.query(History).filter_by(user_id=userid).filter(History.id == historyid).first()
#         history.set_code(response)
            
#         session.commit()
#         session.flush()
#         session.close()
#     except Exception as e:
#         print(e)
        
# def update_history(userid: int, response: str, historyid: int):
#     try:
#         session = SessionLocal()
#         history = session.query(History).filter_by(user_id=userid).filter(History.id == historyid).first()
#         history.set_code(response)
            
#         session.commit()
#         session.flush()
#         session.close()
#     except Exception as e:
#         print(e)
            
        
