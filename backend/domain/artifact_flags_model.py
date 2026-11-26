from sqlalchemy import Boolean, CheckConstraint, Column, Float, ForeignKey, Integer, JSON, String, Table

from core.db import metadata


artifact_flags = Table('artifact_flags', metadata,
    Column('code', String(64), primary_key=True),
    Column('window_code', String(160), ForeignKey('weight_windows.code'), nullable=False),
    Column('score', Float, nullable=False),
    Column('limit_value', Float, nullable=False),
    Column('action', String(160), nullable=False),
    Column('token', String(64), nullable=False, unique=True),
)
