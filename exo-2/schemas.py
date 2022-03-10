from dataclasses import field
from typing import List
import datetime as _dt
from xmlrpc.client import boolean
import pydantic as _pydantic
from pydantic import BaseModel, validator
from sqlalchemy import true

class _contractBase(_pydantic.BaseModel):

    description : str
    date_debut : str
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
        
class contract(_contractBase):
    id : int
    owner_id:int
    
    class Config :
        orm_mode = True

class _Clientbase(_pydantic.BaseModel):
    email:str
     
class ClientCreate(_Clientbase):
    password : str
    
    class Config:
        orm_mode = True
    
class Client(_Clientbase):
    id: int
    date_created = str
    

    class Config :
        orm_mode = True
        

class _Adminbase(_pydantic.BaseModel):
    email:str
    
class AdminCreate(_Adminbase):
    password : str
    
    class Config:
        orm_mode = True
    
class Admin(_Adminbase):
    id: int
    
    class Config :
        orm_mode = True