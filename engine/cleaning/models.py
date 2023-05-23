from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.database import Base


class DataCleaning(Base):
    __tablename__ = "DataCleaning"

    id = Column(Integer, primary_key=True, index=True)

    project = relationship("Project", back_populates="cleaning")
    operations = relationship("Operation", back_populates="cleaning")


class Operation(Base):
    __tablename__ = "Operation"

    id = Column(Integer, primary_key=True, index=True)
    cleaning_id = Column(Integer, ForeignKey("DataCleaning.id"))
    config = Column(String)
    column_subset = Column(String)

    cleaning = relationship("DataCleaning", back_populates="operations")
