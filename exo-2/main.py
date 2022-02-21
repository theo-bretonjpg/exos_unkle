import uvicorn
import  fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import schemas as _schemas 
import services as _services

app = _fastapi.Fastapi()

@app.post("/api/clients")
async def create_client(
    client : _schemas.ClientCreate, db : _orm.Session = _fastapi.Depends(_services.get_db)):
    pass
