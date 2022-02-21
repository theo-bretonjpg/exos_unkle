import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database

class Client(_database.Base):
    __tablename__="client"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String, unique=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    Contract_id = _sql.Column(_sql.Integer, _sql.ForeignKey('contract.id'))
    
    contracts = _orm.relationship('contract', back_populates="client")
        
    def verifie_password_client(self, password : str):
        return _hash.bcrypt.verify(password, self.hashed_password)
    
class Admin(_database.Base):
    __tablename__="admin"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String, unique=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)


def verifie_password_admin(self, password : str):
    return _hash.bcrypt.verify(password, self.hashed_password)

class Contract(_database.Base):
    __tablename__="contract"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    clients_id = _sql.Column(_sql.Integer, _sql.ForeignKey('client.id'))
    description = _sql.Column(_sql.String)
    date_debut = _sql.Column(_sql.DateTime, default=_dt.datetime)
    date_end = _sql.Column(_sql.DateTime, default=_dt.datetime)
    tempete = _sql.column(_sql.Boolean)
    incendie = _sql.column(_sql.Boolean)
    inondation = _sql.column(_sql.Boolean)
    accident = _sql.column(_sql.Boolean)
    vole = _sql.column(_sql.Boolean)


    clients = _orm.relationship('client', back_populates="contract")