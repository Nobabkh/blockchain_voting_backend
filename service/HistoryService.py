from database.databaseConfig.databaseConfig import SessionLocal
from database.entity.User import User
from dto.HistoryDTO import HistoryDTO
from typing import Union
from sqlalchemy import desc, func
from dto.HistorypageDTO import HistorypageDTO
from dto.HistoryListDTO import HistoryListDTO, HistoryListDTOSingle
from database.entity.History import HistoryList, History
from sqlalchemy import desc
from datetime import datetime

    

def gethistorylist(userid: int) -> list[HistoryListDTO]:
    session = SessionLocal()
    histlist_list = session.query(HistoryList).filter_by(user_id=userid).order_by(desc(HistoryList.id)).all()
    historylist = []
    for histlist in histlist_list:
        historylist.append(HistoryListDTO(id=histlist.id, date=histlist.date))
    
    return historylist

def getcurrenthistory(userid: int) -> HistoryListDTO:
    session = SessionLocal()
    historylist = session.query(HistoryList).filter_by(user_id=userid).order_by(desc(HistoryList.id)).first()
    return HistoryListDTO(id=historylist.id, date=historylist.date)

def getdetailedhistory(historyid: int):
    session = SessionLocal()
    historylist = session.query(HistoryList).filter_by(id=historyid).first()
    historylistdto: list[HistoryListDTOSingle] = []
    for history in historylist.histories:
        historylistdto.append(HistoryListDTOSingle(id=history.id, response=history.get_code(), prompttypeimage=history.prompttypeimage, promt=history.promt, promptimg=history.promptimg))
        
    return historylistdto