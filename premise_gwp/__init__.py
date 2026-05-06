__all__ = (
    "add_premise_gwp",
    "check_biosphere_database",
)

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

import bw2data
from bw2io import ExcelLCIAImporter

from .biosphere import (
    LOWER_STRATOSPHERE_CATEGORY,
    check_biosphere_database,
    check_biosphere_version,
    drop_unlinked_flows,
    load_ei310_mapping,
    load_ei311_mapping,
)
from .version import __version__


def use_biosphere_database(biosphere_name):
    previous = bw2data.config.p.get("biosphere_database")
    bw2data.config.p["biosphere_database"] = biosphere_name

    def restore():
        if previous is None:
            try:
                del bw2data.config.p["biosphere_database"]
            except KeyError:
                pass
        else:
            bw2data.config.p["biosphere_database"] = previous

    return restore


def get_flow_name_mapping(biosphere_version):
    mapping = {}

    if biosphere_version >= (0, 8, 12):
        mapping.update(load_ei310_mapping())

    if biosphere_version >= (3, 11):
        mapping.update(load_ei311_mapping())

    return mapping


def apply_flow_name_mapping(category, mapping):
    for method in category.data:
        for flow in method["exchanges"]:
            flow["name"] = mapping.get(flow["name"], flow["name"])


def add_premise_gwp():
    biosphere_name = check_biosphere_database()
    biosphere_version = check_biosphere_version(biosphere_name)
    print(f"Using biosphere database: {biosphere_name} (version {biosphere_version})")

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
        categories_bw2io088 if biosphere_version >= (0, 8, 8) else categories_bw2io087
    )

    for c in categories:
        print("Adding {}".format(c[0]))
        restore_biosphere_database = use_biosphere_database(biosphere_name)
        try:
            category = ExcelLCIAImporter(
                filepath=DATA_DIR / c[-1], name=c[0], unit=c[1], description=c[2]
            )
        finally:
            restore_biosphere_database()

        # if bw2io < 0.8.6
        if biosphere_version < (0, 8, 6):
            if len(list(category.unlinked)) == 1:
                if list(category.unlinked)[0]["name"] == "Carbon dioxide, in air":
                    category.drop_unlinked()

        mapping = get_flow_name_mapping(biosphere_version)
        if mapping:
            print("Converting to ecoinvent 3.10+ biosphere names")
            apply_flow_name_mapping(category, mapping)

        # apply formatting strategies
        category.apply_strategies()

        # check that no flow is unlinked
        if biosphere_version >= (0, 8, 12):
            dropped = drop_unlinked_flows(
                category,
                lambda flow: flow.get("categories") == LOWER_STRATOSPHERE_CATEGORY,
            )
            if dropped:
                print(
                    f"Dropped {dropped} unlinked lower stratosphere + upper "
                    "troposphere flows"
                )

        unlinked = list(category.unlinked)
        if unlinked:
            print(f"{len(unlinked)} unlinked flows:")
            for flow in unlinked:
                print(flow)

            raise ValueError("Unlinked flows")

        # write method
        category.name = c[0]
        category.write_methods(
            overwrite=True,
            verbose=True,
        )
        method = [m for m in bw2data.methods if m == c[0]][0]
        m = bw2data.Method(method)
        m.metadata["name"] = c[0]
