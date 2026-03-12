from datetime import date
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class picklist(Base):
    __tablename__ = 'picklist'

    id = Column(Integer, primary_key=True)
    status = Column(String, default='')
    finishDate = Column(Date, nullable=True)
    priority = Column(String, default='')
    PartNumber = Column(String, nullable=False)
    PKNumber = Column(String, nullable=False)
    WONumber = Column(String, nullable=False)
    Requestor = Column(String, default='')
    intQty = Column(Integer, nullable=False)
    remainQty = Column(Integer, nullable=True)
    salesOrder = Column(String, default='')
    owner = Column(String, default='')
    notes = Column(String, default='')

    __table_args__ = (
        UniqueConstraint('PartNumber', 'PKNumber', name='uix_part_pk'),
    )

class L6L10Parts(Base):
    __tablename__ = 'L6L10Parts'

    PartNumber = Column(String, primary_key=True)

class IMSUpdate(Base):
    __tablename__ = 'IMSUpdate'

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=True)
    PartNumber = Column(String, nullable=False)
    PKNumber = Column(String, nullable=False)
    WONumber = Column(String, nullable=False)
    remainQty = Column(Integer, nullable=False)
