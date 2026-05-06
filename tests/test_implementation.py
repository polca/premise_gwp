from uuid import uuid4

import bw2data
import bw2io

from premise_gwp import add_premise_gwp


def test_implementation():
    """
    Test that the method is properly registered.
    """

    project_name = f"premise-gwp-test-{uuid4().hex}"
    bw2data.projects.set_current(project_name)

    try:
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
        ][0]
        valid_co2_keys = {
            co2_in_air["code"],
            co2_in_air.key,
        }
        if hasattr(co2_in_air, "id"):
            valid_co2_keys.add(co2_in_air.id)

        method = bw2data.Method(new_method)

        assert [cf[1] for cf in method.load() if cf[0] in valid_co2_keys] == [-1]
    finally:
        bw2data.projects.delete_project(project_name, delete_dir=True)
