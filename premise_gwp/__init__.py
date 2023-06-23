__all__ = (
    "add_premise_gwp",
    "check_biosphere_database",
)

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

import bw2io
from bw2io import ExcelLCIAImporter

from .biosphere import check_biosphere_database, check_biosphere_version
from .version import version as __version__


def add_premise_gwp():
    check_biosphere_database()
    bw2io_version = check_biosphere_version()

    # impact methods to create
    categories_bw2io087 = {
        (
            ("IPCC 2013", "climate change", "GWP 20a, incl. H"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for hydrogen",
            "lcia_gwp_20a.xlsx",
        ),
        (
            ("IPCC 2013", "climate change", "GWP 100a, incl. H"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for hydrogen",
            "lcia_gwp_100a.xlsx",
        ),
        (
            ("IPCC 2013", "climate change", "GWP 20a, incl. H and bio CO2"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for hydrogen and biogenic CO2 flows",
            "lcia_gwp_20a_w_bio.xlsx",
        ),
        (
            ("IPCC 2013", "climate change", "GWP 100a, incl. H and bio CO2"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for hydrogen and biogenic CO2 flows",
            "lcia_gwp_100a_w_bio.xlsx",
        ),
    }

    categories_bw2io088 = {
        (
            ("IPCC 2021", "climate change", "GWP 20a, incl. H"),
            "kg CO2-Eq",
            "IPCC 2021, with CFs for hydrogen",
            "lcia_gwp2021_20a.xlsx",
        ),
        (
            ("IPCC 2021", "climate change", "GWP 100a, incl. H"),
            "kg CO2-Eq",
            "IPCC 2021, with CFs for hydrogen",
            "lcia_gwp2021_100a.xlsx",
        ),
        (
            ("IPCC 2021", "climate change", "GWP 20a, incl. H and bio CO2"),
            "kg CO2-Eq",
            "IPCC 2021, with CFs for hydrogen and biogenic CO2 flows",
            "lcia_gwp2021_20a_w_bio.xlsx",
        ),
        (
            ("IPCC 2021", "climate change", "GWP 100a, incl. H and bio CO2"),
            "kg CO2-Eq",
            "IPCC 2021, with CFs for hydrogen and biogenic CO2 flows",
            "lcia_gwp2021_100a_w_bio.xlsx",
        ),
    }

    categories = (
        categories_bw2io088 if bw2io_version >= (0, 8, 8) else categories_bw2io087
    )

    for c in categories:
        print("Adding {}".format(c[0]))
        category = ExcelLCIAImporter(
            filepath=DATA_DIR / c[-1], name=c[0], unit=c[1], description=c[2]
        )

        # apply formatting strategies
        category.apply_strategies()

        # if bw2io < 0.8.6
        if bw2io.__version__ < (0, 8, 6):
            if len(list(category.unlinked)) == 1:
                if list(category.unlinked)[0]["name"] == "Carbon dioxide, in air":
                    category.drop_unlinked()

        # check that no flow is unlinked
        assert len(list(category.unlinked)) == 0, "Unlinked flows: {}".format(
            list(category.unlinked)
        )

        # write method
        category.write_methods(overwrite=True, verbose=True)
