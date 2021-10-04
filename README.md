# `premise_gwp`

Import the official IPCC's GWP100a characterization factors into Brightway2, with the addition of
biogenic CO<sub>2</sub> uptake and release flows. This is needed when using
[premise](https://github.com/romainsacchi/premise) -generated LCI databases that
rely on Bioenergy with carbon capture and storage (BECCS), and any other forms
of storage using biomass. Without it, BECCS operations do not yield a net negative
carbon footprint.

In particular, it adds:
* "Carbon dioxide, in air", with a CF of -1
* "Carbon dioxide, non-fossil", with a CF of +1
* "Carbon dioxide, non-fossil, resource correction", with a CF of +1


The biogenic carbon balance in the rest of the ecoinvent database should be correct.
Hence, using this method, instead of the regular IPCC 2013 GWP100a method, should not
yield any difference, as long as BECCS are not present and solicited in the database.

## Impact category

* IPCC 2013, climate change, GWP 100a, with bio CO2

## Usage

In an open Brightway2 project:
```python
from premise_gwp import add_premise_gwp
add_premise_gwp()
```

## Installation

`pip install premise_gwp`

or

`conda install -c romainsacchi premise_gwp`

