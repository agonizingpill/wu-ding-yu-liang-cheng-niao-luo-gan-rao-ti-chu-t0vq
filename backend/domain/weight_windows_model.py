from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


weight_windows = Table('weight_windows', metadata,
    Column('code', String(64), primary_key=True),
    Column('gauge', String(160), ForeignKey('roof_gauges.code'), nullable=False),
    Column('probes', JSON, nullable=False),
    Column('rain_mm', Float, nullable=False),
    Column('protected', Boolean, nullable=False),
    Column('state', String(160), nullable=False),
    CheckConstraint('rain_mm >= 0'),
)
