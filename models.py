from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

class Signups(Base):
    """
    Example Signups table
    """
    __tablename__ = 'signups'
    id = Column(Integer, primary_key=True)
    nome = Column(String(256))
    mensagem = Column(String(256), unique=True)
    date_signed_up = Column(DateTime())
