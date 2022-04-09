# `premise_gwp`

Import the official IPCC's GWP20a/GWP100a characterization factors into Brightway2, with the addition of
hydrogen and biogenic CO<sub>2</sub> uptake and release flows. This is needed when using
[premise](https://github.com/polca/premise) -generated LCI databases for two reasons:
* in some scenarios, hydrogen-based supply chains (and associated losses) are significant
* some scenarios rely on Bioenergy with carbon capture and storage (BECCS), Direct Air capture (DAC),
and any other forms of storage using biomass or atmospheric resources.
Without it, negative emission technologies (NET) do not yield a net negative
carbon footprint.

## Impact category

This adds:

* IPCC 2013, climate change, GWP 100a, with hydrogen
  * "Hydrogen", with a CF of 33 and 11 for GWP20 and GWP100 respectively.
  
* IPCC 2013, climate change, GWP 100a, with hydrogen and bio CO2
  * "Hydrogen", with a CF of 33 and 11 for GWP20 and GWP100 respectively.
  * "Carbon dioxide, in air", with a CF of -1
  * "Carbon dioxide, non-fossil, resource correction", with a CF of -1
  * "Carbon dioxide, non-fossil", with a CF of +1

The biogenic carbon balance in the rest of the ecoinvent database should be correct.
Hence, using this method, instead of the regular IPCC 2013 GWP100a method, should not
yield any difference, as long as BECCS are not present and solicited in the database.

The characterization factors for the global warming impact GWP100a of for hydrogen 
is taken from [Warwick et al, 2022](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1067144/atmospheric-implications-of-increased-hydrogen-use.pdf).



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

