import bw2data as bd


def check_biosphere_database():
    ERROR = "IPCC LCIA methods for ecoinvent biosphere flows only; install base ecoinvent data"
    assert "biosphere3" in bd.databases, ERROR


def check_biosphere_version() -> tuple:
    # check for the presence of Beryllium II
    if "Beryllium II" not in [f["name"] for f in bd.Database("biosphere3")]:
        bw2io_version = (0, 8, 7)
    else:
        bw2io_version = (0, 8, 8)

    return bw2io_version
