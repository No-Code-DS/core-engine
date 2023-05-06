from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.database import Base


class FeatureEngineering(Base):
    __tablename__ = "FeatureEngineering"

    id = Column(Integer, primary_key=True, index=True)

    project = relationship("Project", back_populates="feature_engineering")
    features = relationship("Feature", back_populates="fe")


class Feature(Base):
    __tablename__ = "Feature"

    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String)
    feature_expression = Column(String)
    feature_engineering_id = Column(Integer, ForeignKey("FeatureEngineering.id"))

    fe = relationship("FeatureEngineering", back_populates="features")
