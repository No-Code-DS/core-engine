from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.database import Base


class Deployment(Base):
    __tablename__ = "Deployment"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String)

    project = relationship("Project", back_populates="deployment", uselist=False)
