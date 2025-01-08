
from database.databaseConfig.databaseConfig import Base, engine
def Migrate():
    Base.metadata.create_all(bind=engine)