"""Generate figures with the weather briefing library."""

from typing import Callable, Iterator, Union
from PIL import Image as img
from matplotlib.figure import Figure
import pandas as pd
import xarray as xr

import intake

from wblib.figures.hifs import HifsForecasts
from wblib.services._define_figures import EXTERNAL_INST_PLOTS
from wblib.services._define_figures import EXTERNAL_LEAD_PLOTS
from wblib.services._define_figures import INTERNAL_PLOTS
from wblib.services._define_figures import PLOTS_LEADTIMES

Image = Union[img.Image, Figure]

INTAKE_CATALOG_URL = "https://tcodata.mpimet.mpg.de/internal.yaml"
MAX_LEAD_TIME_EXTERNAL_LEAD = 120   #[h]

def generate_external_inst_figures(
    current_location: str,
    current_time: pd.Timestamp,
    briefing_time: pd.Timestamp,
    sattracks_fc_time: pd.Timestamp,
    meteor_track: xr.Dataset,
    logger: Callable
) -> Iterator[tuple[str, Image]]:
    for product, function in EXTERNAL_INST_PLOTS.items():
        if function is None:
            _warn_function_is_not_defined(product, logger)
            continue
        try:
            figure = function(
                current_time,
                briefing_time,
                sattracks_fc_time,
                current_location,
                meteor_track,
                )
            yield (product, figure)
        except Exception as error:
            msg = (
                f"Can not generate {product} with '{current_time}'. "
                "Please provide it manually or debug the code."
            )
            logger(msg, "ERROR")
            print(error)
            continue


def generate_external_lead_figures(
    briefing_time: pd.Timestamp,
    current_time: pd.Timestamp,
    sattracks_fc_time: pd.Timestamp,
    logger: Callable
) -> Iterator[tuple[str, str, Image]]:
    for product, function in EXTERNAL_LEAD_PLOTS.items():
        if function is None:
            _warn_function_is_not_defined(product, logger)
            continue
        for lead_hours in PLOTS_LEADTIMES:
            if int(lead_hours[:-1]) > MAX_LEAD_TIME_EXTERNAL_LEAD:
                continue
            try:
                figure = function(
                    briefing_time,
                    lead_hours,
                    current_time,
                    sattracks_fc_time,
                )
                yield (product, lead_hours, figure)
            except Exception as error:
                msg = (
                    f"Can not generate {product} with '{current_time}' "
                    f"and '{lead_hours}'. Please provide it manually or "
                    "debug the code."
                )
                logger(msg, "ERROR")
                print(error)
                continue


def generate_internal_figures(
    briefing_time: pd.Timestamp,
    current_time: pd.Timestamp,
    sattracks_fc_time: pd.Timestamp,
    meteor_track: xr.Dataset,
    logger: Callable
) -> Iterator[tuple[str, str, Image]]:
    catalog = intake.open_catalog(INTAKE_CATALOG_URL)
    hifs = HifsForecasts(catalog)
    for product, function in INTERNAL_PLOTS.items():
        if function is None:
            _warn_function_is_not_defined(product, logger)
            continue
        for lead_hours in PLOTS_LEADTIMES:
            try:
                figure = function(
                    briefing_time,
                    lead_hours,
                    current_time,
                    sattracks_fc_time,
                    meteor_track,
                    hifs
                )
                figure.tight_layout(pad=1.01)
                yield (product, lead_hours, figure)
            except Exception as error:
                msg = (
                    f"Can not generate {product} with '{current_time}' "
                    f"and '{lead_hours}'. Please provide it manually or "
                    "debug the code."
                    # f"Given briefing time: {briefing_time}"
                    # f"Given Meteor track: {meteor_track}"
                    # f"Given sattracks_fc_time: {sattracks_fc_time}"
                )
                logger(msg, "ERROR")
                print(error)
                continue


def _warn_function_is_not_defined(product, logger):
    msg = f"Undefined function for '{product}' product."
    logger(msg, "ERROR")

if __name__ == "__main__":
    def logger(message: str, level: str) -> None:
        return None
    sattracks_fc_time = pd.Timestamp(2024, 8, 5).tz_localize("UTC")
    briefing_time1 = pd.Timestamp(2024, 8, 11).tz_localize("UTC")
    current_time1 = pd.Timestamp(2024, 8, 11).tz_localize("UTC")
    figures = generate_internal_figures(
        briefing_time1, current_time1, sattracks_fc_time, logger)
    next(figures)
