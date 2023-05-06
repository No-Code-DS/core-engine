from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.database import Base


class DataCleaning(Base):
    __tablename__ = "DataCleaning"

    id = Column(Integer, primary_key=True, index=True)

    project = relationship("Project", back_populates="cleaning")
    formulas = relationship("Formula", back_populates="cleaning")


class Formula(Base):
    __tablename__ = "Formula"

    id = Column(Integer, primary_key=True, index=True)
    cleaning_id = Column(Integer, ForeignKey("DataCleaning.id"))
    formula_string = Column(String)
    target_column = Column(String)

    cleaning = relationship("DataCleaning", back_populates="formulas")
