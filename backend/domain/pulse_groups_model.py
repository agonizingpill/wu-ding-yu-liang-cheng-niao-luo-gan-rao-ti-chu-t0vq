from sqlalchemy import Column, Float, ForeignKey, JSON, String, Table

from core.db import metadata


pulse_groups = Table('pulse_groups', metadata,
    Column('code', String(64), primary_key=True),
    Column('gauge', String(160), ForeignKey('roof_gauges.code'), nullable=False),
    Column('windows', JSON, nullable=False),
    Column('baseline', JSON, nullable=False),
    Column('scores', JSON, nullable=False),
    Column('limit_value', Float, nullable=False),
    Column('status', String(160), nullable=False),
    Column('flag', String(160), ForeignKey('artifact_flags.code'), nullable=True),
    Column('rain', String(160), ForeignKey('rain_series.code'), nullable=True),
)
