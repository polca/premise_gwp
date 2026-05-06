from types import SimpleNamespace

from premise_gwp.biosphere import (
    LOWER_STRATOSPHERE_CATEGORY,
    drop_unlinked_flows,
    load_ei311_mapping,
)


def test_load_ei311_mapping():
    mapping = load_ei311_mapping()

    assert mapping["Methane, bromo-, Halon 1001"] == "Bromomethane"
    assert (
        mapping["Methane, bromochlorodifluoro-, Halon 1211"]
        == "Bromochlorodifluoromethane"
    )
    assert (
        mapping["Methane, bromotrifluoro-, Halon 1301"]
        == "Bromotrifluoromethane"
    )


def test_drop_unlinked_flows_only_drops_matching_unlinked_flows():
    importer = SimpleNamespace(
        data=[
            {
                "exchanges": [
                    {
                        "name": "Linked flow",
                        "input": ("biosphere3", "abc"),
                        "categories": LOWER_STRATOSPHERE_CATEGORY,
                    },
                    {
                        "name": "Dropped flow",
                        "categories": LOWER_STRATOSPHERE_CATEGORY,
                    },
                    {
                        "name": "Kept flow",
                        "categories": ("air",),
                    },
                ]
            }
        ]
    )

    dropped = drop_unlinked_flows(
        importer, lambda flow: flow.get("categories") == LOWER_STRATOSPHERE_CATEGORY
    )

    assert dropped == 1
    assert [flow["name"] for flow in importer.data[0]["exchanges"]] == [
        "Linked flow",
        "Kept flow",
    ]
