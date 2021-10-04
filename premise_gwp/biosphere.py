import bw2data as bd


def check_biosphere_database():
    ERROR = "IPCC LCIA methods for ecoinvent biosphere flows only; install base ecoinvent data"
    assert "biosphere3" in bd.databases, ERROR
