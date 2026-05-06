from pathlib import Path

import bw2data as bd
import yaml

DATA_DIR = Path(__file__).resolve().parent / "data"
LOWER_STRATOSPHERE_CATEGORY = ("air", "lower stratosphere + upper troposphere")


def load_mapping(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as stream:
        mappings = yaml.safe_load(stream)
    return mappings


def load_ei310_mapping():
    return load_mapping("mapping_ei310.yaml")


def load_ei311_mapping():
    return load_mapping("mapping_ei311.yaml")


def get_biosphere_database_candidates():
    return sorted(
        name
        for name in bd.databases
        if "biosphere" in name.lower() and "spatialized" not in name.lower()
    )


def check_presence_biosphere_database(biosphere_name: str) -> str:
    """
    Check that the biosphere database is present in the current project.
    """

    if biosphere_name in bd.databases:
        return biosphere_name

    if bd.config.biosphere in bd.databases:
        return bd.config.biosphere

    candidates = get_biosphere_database_candidates()
    if len(candidates) == 1:
        return candidates[0]

    print("`premise_gwp` requires the name of your biosphere database.")
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
    flow_names = {f["name"] for f in bd.Database(biosphere_name)}

    if "3.12" in biosphere_name:
        return (3, 12)

    if "3.11" in biosphere_name:
        return (3, 11)

    if "3.10" in biosphere_name:
        return (3, 10)

    if "Bromomethane" in flow_names and "Methane, bromo-, Halon 1001" not in flow_names:
        return (3, 11)

    # check for the presence of Beryllium II
    if "Beryllium II" not in flow_names:
        if "Carbon dioxide, in air" not in flow_names:
            biosphere_version = (0, 8, 5)
        else:
            biosphere_version = (0, 8, 6)
    else:
        if "Methylchloride" in flow_names:
            biosphere_version = (0, 8, 12)
        else:
            biosphere_version = (0, 8, 8)

    return biosphere_version


def drop_unlinked_flows(importer, predicate):
    dropped = 0

    for method in importer.data:
        exchanges = []
        for exchange in method.get("exchanges", []):
            if not exchange.get("input") and predicate(exchange):
                dropped += 1
            else:
                exchanges.append(exchange)
        method["exchanges"] = exchanges

    return dropped
