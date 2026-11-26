from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


rain_series = Table('rain_series', metadata,
    Column('code', String(64), primary_key=True),
    Column('gauge', String(160), ForeignKey('roof_gauges.code'), nullable=False),
    Column('flag', String(160), ForeignKey('artifact_flags.code'), nullable=False, unique=True),
    Column('total', Float, nullable=False),
    Column('n_windows', Integer, nullable=False),
    Column('omitted', Integer, nullable=False),
    CheckConstraint('total >= 0'),
    CheckConstraint('omitted >= 0'),
    CheckConstraint('n_windows >= 0'),
)
