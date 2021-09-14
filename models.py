from sqlalchemy import Column,Integer,Numeric,String

from database import Base

class Crypto(Base):
    __tablename__ = "crypto"

    id = Column(Integer,primary_key=True,index=True)
    symbol = Column(String,unique=True,index=True)
    open =Column(Numeric(10,2))
    high =Column(Numeric(10,2))
    low =Column(Numeric(10,2))
    close =Column(Numeric(10,2))
    volume =Column(Numeric(10,2))