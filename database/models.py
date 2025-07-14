from sqlalchemy import Column, Integer, Text, BigInteger, Boolean

from database.base import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    refer_start = Column(Text, nullable=True)
    my_refer_url = Column(Text, nullable=True)
    active = Column(Integer, nullable=True, default=1)
    dialogs = Column(Text, nullable=True)
    sum_vivod = Column(BigInteger, default=0)
    sum_itog = Column(BigInteger, default=0)
    free_day = Column(Integer, nullable=True)
    zapros_count = Column(Integer, default=2)
    state = Column(Text, nullable=True)
    review = Column(Integer, default=0)

class Subscribe(Base):
    __tablename__ = 'subscribe'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    time_sub = Column(BigInteger, unique=False)