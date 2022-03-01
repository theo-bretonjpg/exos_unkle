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
    
