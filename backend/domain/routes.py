from domain.roof_gauges_api import router as roof_gauges
from domain.weight_windows_api import router as weight_windows
from domain.artifact_flags_api import router as artifact_flags
from domain.rain_series_api import router as rain_series

routers = (roof_gauges, weight_windows, artifact_flags, rain_series,)
