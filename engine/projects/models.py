import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..db.database import Base


class UserProject(Base):
    __tablename__ = "UserToProject"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    project_id = Column(Integer, ForeignKey("Projects.id", ondelete="CASCADE"))


class Project(Base):
    __tablename__ = "Projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, default="unnamed project")
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    data_source_id = Column(Integer, ForeignKey("DataSources.id", ondelete="SET NULL"))
    cleaning_id = Column(Integer, ForeignKey("DataCleaning.id", ondelete="SET NULL"))
    feature_engineering_id = Column(Integer, ForeignKey("FeatureEngineering.id", ondelete="SET NULL"))
    model_id = Column(Integer, ForeignKey("SelectedModel.id", ondelete="SET NULL"))

    users = relationship("User", secondary="UserToProject", back_populates="projects")
    data_source = relationship("DataSource", back_populates="project", uselist=False)
    cleaning = relationship("DataCleaning", back_populates="project", uselist=False)
    feature_engineering = relationship("FeatureEngineering", back_populates="project", uselist=False)


class DataSource(Base):
    __tablename__ = "DataSources"

    id = Column(Integer, primary_key=True, index=True)
    data_source_name = Column(String)
    file_path = Column(String)
    project = relationship("Project", back_populates="data_source")


class FeatureEngineering(Base):
    __tablename__ = "FeatureEngineering"

    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(Integer, ForeignKey("Feature.id"))
    project = relationship("Project", back_populates="feature_engineering")


class Feature(Base):
    __tablename__ = "Feature"

    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String)
    feature_expression = Column(String)


class SelectedModel(Base):
    __tablename__ = "SelectedModel"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String)
