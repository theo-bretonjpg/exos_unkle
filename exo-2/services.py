from http import client
import fastapi.security as _security
from sqlalchemy import false
import database as _database
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import email_validator as _email_check
import fastapi as _fastapi
import passlib.hash as  _hash
import jwt as _jwt


_JWT_SECRET = "thisisnotverys"

oauth2schemaadmin = _security.OAuth2PasswordBearer("/api/admin/token")

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

async def get_admin_by_email(email: str, db: _orm.session):
    return db.query(_models.Admin).filter(_models.Admin.email == email).first()

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
"""
async def create_admin(admin: _schemas.AdminCreate, db: _orm.Session):
    # check that email is valid
    try:
        valid = _email_check.validate_email(email=admin.email)
        
        email = valid.email
    except _email_check.EmailNotValidError:    
        raise _fastapi.HTTPException(
            status_code=404, detail="Please enter a valid email"
        )

    hashed_password = _hash.bcrypt.hash(admin.password)
    admin_obj = _models.Admin(email=email, hashed_password=hashed_password)
    
    db.add(admin_obj)
    db.commit()
    db.refresh(admin_obj)
    return admin_obj
    """

"""
#creating a token for admin
async def create_admin_token(admin: _models.Admin):
    admin_schema_obj = _schemas.Admin.from_orm(admin)
    
    Admin_dict = admin_schema_obj.dict()

    token = _jwt.encode(
        Admin_dict, _JWT_SECRET)
    
    return dict(access_token=token, token_type="bearer")
"""
#creating a token for client

async def create_client_token(client: _models.Client):
    admin_schema_obj = _schemas.Client.from_orm(client)
    
    Client_dict = admin_schema_obj.dict()

    
    token = _jwt.encode(
        Client_dict, _JWT_SECRET)
    
    return dict(access_token=token, token_type="bearer")
    

async def authenticate_user(email : str, password : str, db: _orm.Session):
    Client = await get_user_by_email(email=email, db=db)  

    if not Client :
        return False

    if not Client.verify_password_client(password=password):
        return False
    
    return Client

async def authenticate_admin(email : str, password : str, db: _orm.Session):
    Admin = await get_admin_by_email(email=email, db=db)  

    if not Admin :
        return False

    if not Admin.verify_password_admin(password=password):
        return False
    
    return Admin



async def get_current_admin(db: _orm.Session=_fastapi.Depends(get_db), token: str=_fastapi.Depends(oauth2schemaadmin),
):
    try :
        payload= _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        client = db.query(_models.Client).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="invalid email or password"
        )

    return _schemas.Client.from_orm(client)


async def create_contract(client: _schemas.Client, db: _orm.Session, contract: _schemas._contractCreate):
    contract = _models.Contract(**contract.dict(), client_id=client.id)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return _schemas.Contract.from_orm(contract)

async def get_all_client_contracts(client: _schemas.Client, db: _orm.Session):
    contracts = db.query(_models.Contract).filter_by(client_id=client.id)

    return list(map(_schemas.Contract.from_orm, contracts))

