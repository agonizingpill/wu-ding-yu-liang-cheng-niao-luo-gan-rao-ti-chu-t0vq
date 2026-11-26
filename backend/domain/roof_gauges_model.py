from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


roof_gauges = Table('roof_gauges', metadata,
    Column('code', String(64), primary_key=True),
    Column('building', String(160), nullable=False),
    Column('tared', Boolean, nullable=False),
    Column('window', String(160), nullable=False),
)
