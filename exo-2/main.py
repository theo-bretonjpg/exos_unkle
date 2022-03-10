from typing import List
import uvicorn
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import schemas as _schemas 
import services as _services

app = _fastapi.FastAPI()

#gets all information of clients (for admins only)
@app.get("/api/admin/all-clients/", response_model= list[_schemas.Client])
async def get_clients(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),admin = _fastapi.Depends(_services.get_current_admin)):
    clients = _services.get_clients(db=db, skip=skip, limit=limit)
    return clients


#get information on me (for clients)
@app.get("/api/clients/{client_id}", response_model=_schemas.Client)
def read_client(client_id: int, db: _orm.Session=_fastapi.Depends(_services.get_db)):
    db_client = _services.read_client(db=db, client_id=client_id)
    if db_client is None : 
        raise _fastapi.HTTPException(status_code=404, detail="sorry this user does not exist")

    return db_client

#Create a client
@app.post("/api/admin/clients")

async def create_client(
    client : _schemas.ClientCreate, db: _orm.Session=_fastapi.Depends(_services.get_db),
    admin = _fastapi.Depends(_services.get_current_admin)):
    db_client = await _services.get_user_by_email(email=client.email, db=db)
    if db_client : 
        raise _fastapi.HTTPException(
            status_code=400, detail="client with that email already exists"
        )

    #create the client user
    client = await _services.create_client(client=client, db=db)
    #return token
    return await _services.create_client_token(client=client)


#creates client token 
@app.post("/api/client/token")

async def generate_client_token(

    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    client = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not client:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_client_token(client=client)



#Create Contract
@app.post("/api/admin/{client_id}/contracts", response_model=_schemas.Contract)
async def create_contract(
    client_id : int, contract: _schemas._contractCreate, 
    db: _orm.Session=_fastapi.Depends(_services.get_db),
    admin = _fastapi.Depends(_services.get_current_admin)):
    db_client = _services.read_client(db=db, client_id=client_id)
    if db_client is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user doesn t exist"
        )
    return _services.create_contract(db=db, contract=contract, client_id=client_id) 

#    contract: _schemas._contractCreate, form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
#    db: _orm.Session = _fastapi.Depends(_services.get_db), 
#    admin = _fastapi.Depends(_services.get_current_admin)):
    
#    client = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db),
    
#    if not client:
#        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")


#    return await _services.create_contract(client=client, db=db, contract=contract)


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

@app.post("/api/admin/token")

async def generate_admin_token(

    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    admin = await _services.authenticate_admin(email=form_data.username, password=form_data.password, db=db)

    if not admin:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_admin_token(admin=admin)
