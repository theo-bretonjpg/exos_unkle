from typing import List
import uvicorn
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import schemas as _schemas 
import services as _services

app = _fastapi.FastAPI()

#Create a client
@app.post("/api/clients")
async def create_client(
    
    client : _schemas.ClientCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_client = await _services.get_user_by_email(email=client.email, db=db)
    if db_client : 
        raise _fastapi.HTTPException(
            status_code=400, detail="user with that email already exists"
        )

    #create the client user
    client = await _services.create_client(client=client, db=db)
    #return token
    return await _services.create_client_token(client=client)

#Create a admin
@app.post("/api/admin")
async def create_admin(
    admin : _schemas.AdminCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_admin = await _services.get_admin_by_email(email=admin.email, db=db)
    if db_admin : 
        raise _fastapi.HTTPException(
            status_code=400, detail="user with that email already exists"
        )

    #create the client user
    admin = await _services.create_admin(admin=admin, db=db)
    #return token
    return await _services.create_admin_token(admin=admin)


#sees all information on client

@app.post("/api/admin/token")

async def generate_admin_token(

    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    admin = await _services.authenticate_admin(email=form_data.username, password=form_data.password, db=db)

    if not admin:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_admin_token(admin=admin)

@app.post("/api/client/token")

async def generate_client_token(

    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    client = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not client:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_client_token(client=client)


@app.get("/api/clients/me", response_model= _schemas.Client)
async def get_client(client: _schemas.Client = _fastapi.Depends(_services.get_current_client)):
    return client


#Create Contract
@app.post("/api/contracts", response_model=_schemas.Contract)
async def create_contract(contract: _schemas._contractCreate, client: _schemas.Client = _fastapi.Depends(_services.get_current_admin), 
db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_contract(client=client, db=db, contract=contract)


#sees client contracts
@app.get("/api/admin/contracts", response_model=list[_schemas.Contract])
async def get_client_contracts(
    client: _schemas.Client = _fastapi.Depends(_services.get_current_admin),
     form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db : _orm.Session = _fastapi.Depends(_services.get_db)):

    admin = await _services.authenticate_admin(email=form_data.username, password=form_data.password, db=db)

    if not admin:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials you are not an admin")

    await _services.get_all_client_contracts(client=client, db=db)

