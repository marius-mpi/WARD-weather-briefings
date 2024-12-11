from orcestra.sat import SattrackLoader
import pandas as pd

satellite = "EARTHCARE"
kind = "PRE"
roi = "BARBADOS"

SattrackLoader(satellite, '2024-12-10', kind=kind, roi=roi).get_track_for_day(valid_time)