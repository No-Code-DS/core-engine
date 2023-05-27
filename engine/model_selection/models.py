import enum

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from ..db.database import Base


class StatusEnum(enum.Enum):
    TRAINING = "Training"
    TRAINED = "Trained"
    FAILED = "Failed"
    DEPLOYED = "Deployed"


class SelectedModel(Base):
    __tablename__ = "SelectedModel"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    prediction_field = Column(String, nullable=False)
    config = Column(String, nullable=False)
    status = Column(ENUM(StatusEnum))
    evaluation = Column(String)

    project = relationship("Project", back_populates="model")
