from pathlib import Path

import bw2data as bd
import yaml

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_ei310_mapping():
    with open(DATA_DIR / "mapping_ei310.yaml", "r", encoding="utf-8") as stream:
        mappings = yaml.safe_load(stream)
    return mappings


def check_presence_biosphere_database(biosphere_name: str) -> str:
    """
    Check that the biosphere database is present in the current project.
    """

    if biosphere_name not in bd.databases:
        print("RELICS requires the name of your biosphere database.")
        print(
            "Please enter the name of your biosphere database as it appears in your project."
        )
        print(bd.databases)
        biosphere_name = input("Name of the biosphere database: ")

    return biosphere_name


def check_biosphere_database():
    biosphere_name = check_presence_biosphere_database("biosphere3")
    ERROR = "IPCC LCIA methods for ecoinvent biosphere flows only; install base ecoinvent data"
    assert biosphere_name in bd.databases, ERROR
    return biosphere_name


def check_biosphere_version(biosphere_name) -> tuple:
    # check for the presence of Beryllium II
    if "Beryllium II" not in [f["name"] for f in bd.Database(biosphere_name)]:
        bw2io_version = (0, 8, 7)
    else:
        if "Methylchloride" in [f["name"] for f in bd.Database(biosphere_name)]:
            bw2io_version = (0, 8, 12)
        else:
            bw2io_version = (0, 8, 8)

    return bw2io_version
