import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas



def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db=_database.SessionLocal()
    try:
        yield db
    finally:
        db.close
        
async def get_user_by_email(email: str, db: _orm.session):
    return db.query(_models.Client).filter(_models.Client.email == email).first()

async def create_client=(client: _schemas.ClientCreate, db: _orm.Session):
    #check that email is valid
    
