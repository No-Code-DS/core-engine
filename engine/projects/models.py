from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..db.database import Base


class UserToProject(Base):
    __tablename__ = "UserToProject"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    workflow_id = Column(Integer, ForeignKey("Projects.id", ondelete="CASCADE"))


class Project(Base):
    __tablename__ = "Projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String)
    created_at = DateTime()
    data_source_id = Column(Integer, ForeignKey("DataSources.id", ondelete="CASCADE"))
    cleaning_id = Column(Integer, ForeignKey("DataCleaning.id", ondelete="CASCADE"))
    feature_engineering_id = Column(Integer, ForeignKey("FeatureEngineering.id", ondelete="CASCADE"))
    model_id = Column(Integer, ForeignKey("SelectedModel.id", ondelete="CASCADE"))


class DataSource(Base):
    __tablename__ = "DataSources"

    id = Column(Integer, primary_key=True, index=True)
    data_source_name = Column(String)
    file_path = Column(String)


class DataCleaning(Base):
    __tablename__ = "DataCleaning"

    id = Column(Integer, primary_key=True, index=True)
    formula_id = Column(Integer, ForeignKey("Formula.id"))


class Formula(Base):
    __tablename__ = "Formula"

    id = Column(Integer, primary_key=True, index=True)
    formula_string = Column(String)
    target_column = Column(String)


class FeatureEngineering(Base):
    __tablename__ = "FeatureEngineering"

    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey("Feature.id"))


class Feature(Base):
    __tablename__ = "Feature"

    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String)
    feature_expression = Column(String)


class SelectedModel(Base):
    __tablename__ = "SelectedModel"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String)