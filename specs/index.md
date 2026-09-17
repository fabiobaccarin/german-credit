# German credit score specification files

This file summarizes the specification and provides links to detailed
specification files.

## Module: data

**File:** `scr/german_credit/data.py`

The `data` module provides domain models and functionality for reading, writing,
validating and fetching data. The user creates a new `Dataset` object that
stores information about to fetch and validate data from the internet or from
disk. The `Dataset` object is responsible for validating all inputs necessary
to safely perform operations with the `data` module's functionality.

With a `Dataset` object, the user can perform simple operations on it, such as
`read`, and `write` Polars Dataframe objects.

Example:

```python
from german_credit import data

dataset = data.Dataset(
    content_url="http://foo.com/bar.pq",
    checksum="some-hash-string",
    file="path-to-file.parquet"
)

df = data.read(dataset)
data.write(df, dataset)
```

