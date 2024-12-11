import xarray as xr
from wblib.figures.briefing_info import INTERNAL_FIGURE_SIZE, get_climatology_path


VARIABLES = ["tcwv"]
CATALOG_URL = "https://tcodata.mpimet.mpg.de/internal.yaml"
CLIMATOLOGY_CUT_OUT_TIME = "2023-01-01"
CLIMATOLOGY_FILE = "hera5_climatology.nc"


def download_hera5_climatology():
    hera5 = get_hera5_climatology()
    hera5_climatology_path = str(resources.files(wblib) / CLIMATOLOGY_FILE)
    hera5.to_netcdf(hera5_climatology_path)
    
download_hera5_climatology()
# climatology_path = get_climatology_path()
# climatology = xr.open_dataset(climatology_path)

# print(climatology.dayofyear)


# path = '/Users/mschulz/Documents/HPC&Coding/weather/src/wblib/figures/data/hera5_climatology.nc'

# climatology2 = xr.open_dataset(path)

# print(climatology2.dayofyear)