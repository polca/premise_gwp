import bw2data
import bw2io

from premise_gwp import add_premise_gwp


def test_implementation():
    """
    Test that the method is properly registered.
    """

    bw2data.projects.set_current("test")
    bw2io.create_default_biosphere3()

    add_premise_gwp()

    # check that the new method exists
    new_method = ("IPCC 2021", "climate change", "GWP 100a, incl. H and bio CO2")
    assert new_method in bw2data.methods

    # check that "Carbon dioxide, in air" has now a CF of -1

    co2_in_air = [
        f
        for f in bw2data.Database("biosphere3")
        if "carbon dioxide, in air" in f["name"].lower()
    ][0]["code"]

    method = bw2data.Method(new_method)

    for cf in method.load():
        if cf[0] == co2_in_air:
            assert cf[1] == -1
