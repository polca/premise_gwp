__all__ = (
    "add_premise_gwp",
    "check_biosphere_database",
)

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

from .version import version as __version__
from bw2io import ExcelLCIAImporter
from .biosphere import check_biosphere_database


def add_premise_gwp():
    check_biosphere_database()

    categories = {
        (
            ("IPCC 2013", "climate change", "GWP 20a, incl. bio CO2"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for biogenic CO2 flows",
            "lcia_gwp_20a.xlsx",
        ),
        (
            ("IPCC 2013", "climate change", "GWP 100a, incl. bio CO2"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for biogenic CO2 flows",
            "lcia_gwp_100a.xlsx",
        ),
        (
            ("IPCC 2013", "climate change", "GTP 20a, incl. bio CO2"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for biogenic CO2 flows",
            "lcia_gtp_20a.xlsx",
        ),
        (
            ("IPCC 2013", "climate change", "GTP 100a, incl. bio CO2"),
            "kg CO2-Eq",
            "IPCC 2013, with CFs for biogenic CO2 flows",
            "lcia_gtp_100a.xlsx",
        ),
    }

    for c in categories:
        print("Adding {}".format(c[0]))
        category = ExcelLCIAImporter(
            filepath=DATA_DIR / c[-1], name=c[0], unit=c[1], description=c[2]
        )
        category.apply_strategies()
        assert len(list(category.unlinked)) == 0
        category.write_methods(overwrite=True, verbose=True)