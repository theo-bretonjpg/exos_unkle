from typing import List
import uvicorn
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import schemas as _schemas 
import services as _services

app = _fastapi.FastAPI()

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
    return await _services.create_token(client=client)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    
    client = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not client:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(client=client)

@app.get("/api/clients/me", response_model= _schemas.Client)
async def get_client(client: _schemas.Client = _fastapi.Depends(_services.get_current_client)):
    return client    

@app.post("/api/contracts", response_model=_schemas.Contract)
async def create_contract(contract: _schemas._contractCreate, client: _schemas.Client = _fastapi.Depends(_services.get_current_client), 
db: _orm.Session=_fastapi.Depends(_services.get_db)):
    return await _services.create_contract(client=client, db=db, contract=contract)

@app.get("/api/contracts", response_model=list[_schemas.Contract])
async def get_client_contracts(
    client: _schemas.Client = _fastapi.Depends(_services.get_current_client),
    db : _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_client_contracts(client=client, db=db)