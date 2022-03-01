import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import email_validator as _email_check
import fastapi as _fastapi
import passlib.hash as  _hash
import jwt as _jwt


_JWT_SECRET = "thisisnotverys"

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

async def create_client(client: _schemas.ClientCreate, db: _orm.Session):
    # check that email is valid
    try:
        valid = _email_check.validate_email(email=client.email)
        
        email = valid.email
    except _email_check.EmailNotValidError:    
        raise _fastapi.HTTPException(
            status_code=404, detail="Please enter a valid email"
        )
    hashed_password = _hash.bcrypt.hash(client.password)
    client_obj = _models.Client(email=email, hashed_password=hashed_password)
    
    db.add(client_obj)
    db.commit()
    db.refresh(client_obj)
    return client_obj
    
   #creating a token for client
    
async def create_token(client: _models.Client):
    client_schema_obj = _schemas.Client.from_orm(client)
    
    client_dict = client_schema_obj.dict()
    #del client_dict["date_created"]
    
    token = _jwt.encode(
        client_dict, _JWT_SECRET)
    
    return dict(access_token=token, token_type="bearer")
    
    
