from sqlalchemy import JSON, Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


class ClinVarVariant(Base):
    __tablename__ = "clinvar_variants"

    id = Column(Integer, primary_key=True)
    gene = Column(String(64), nullable=False, index=True)
    variant = Column(String(128), nullable=False, index=True)
    pathogenicity = Column(String(32), nullable=False)
    effect_size = Column(String(32), nullable=False, default="1.0")


class CachedRiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True)
    patient_hash = Column(String(64), nullable=False, unique=True)
    payload = Column(JSON, nullable=False)


class SeroprevalenceReference(Base):
    __tablename__ = "seroprevalence_reference"

    id = Column(Integer, primary_key=True)
    cohort = Column(String(64), nullable=False, index=True)
    virus = Column(String(32), nullable=False)
    seropositivity_rate = Column(String(32), nullable=False)


class SpinGlassLandscape(Base):
    __tablename__ = "spin_glass_landscapes"

    id = Column(Integer, primary_key=True)
    landscape_key = Column(String(64), nullable=False, unique=True)
    payload = Column(JSON, nullable=False)


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
