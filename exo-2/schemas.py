import datetime as _dt
from xmlrpc.client import boolean
import pydantic as _pydantic

class _Clientbase(_pydantic.BaseModel):
    email:str
     
class ClientCreate(_Clientbase):
    password : str
    
    class Config:
        orm_mode = True
    
class Client(_Clientbase):
    id: int
    date_created = _dt.datetime
    
    class Config :
        orm_mode = True
        

class _Adminbase(_pydantic.BaseModel):
    email:str
    date_created : str
    
class AdminCreate(_Adminbase):
    password : str
    
    class Config:
        orm_mode = True
    
class Admin(_Adminbase):
    id: int
    date_created: _dt.datetime
    
    class Config :
        orm_mode = True
        
class _contractBase(_pydantic.BaseModel):

    description : str
    date_debut : _dt.datetime
    date_end : str
    tempete : bool
    incendie : bool
    inondation : bool
    accident : bool
    vole : bool
    
class _contractCreate(_contractBase):
    pass

    class Config :
        orm_mode = True
        

class Contract(_contractBase):
    
    id : int
    client_id:int
    
    class Config :
        orm_mode = True
    