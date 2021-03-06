import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database

class Client(_database.Base):
    __tablename__="client"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.String)

    contracts = _orm.relationship('Contract', back_populates="owner")
        
    def verify_password_client(self, password : str):
        return _hash.bcrypt.verify(password, self.hashed_password)
    
class Admin(_database.Base):
    __tablename__="admin"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.String)

    def verify_password_admin(self, password : str):
        return _hash.bcrypt.verify(password, self.hashed_password)

class Contract(_database.Base):
    __tablename__="contracts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    description = _sql.Column(_sql.String)
    date_debut = _sql.Column(_sql.String)
    date_end = _sql.Column(_sql.String)
    tempete = _sql.Column(_sql.Boolean)
    incendie = _sql.Column(_sql.Boolean)
    inondation = _sql.Column(_sql.Boolean)
    accident = _sql.Column(_sql.Boolean)
    vole = _sql.Column(_sql.Boolean)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey('client.id'))

    owner = _orm.relationship('Client', back_populates="contracts")