# Data service specification

This file describes the project's data service API.

**Summary:** The data service is implemented as a module of Python functions for
reading, writing and validating data. The service implements domain models to
represent data and provide validation.

**File:** `src/german_credit/data.py`

## Domain models

All types mentioned and not described in this file have one of these 
characteristics:

1. It is a primitive data type provided by Python's standard library;
2. It is a data type provided by a third party library like Pydantic.

### MD5ChecksumString

An annotated type based on a string with proper MD5 hexadecimal representation
constraints.

### Dataframe

An alias for a Polars DataFrame.

### Dataset

An immutable Pydantic model representing dataset metadata.

**Attributes:**
- `url`: an object of type `HttpUrl` or `None` that represent's the dataset's
  URL. It must accept a HTTP GET request if provided;
- `checksum`: an object of type `MD5ChecksumString` or `None` that is used to 
  verify the data's integrity if downloaded from the web;
- `filepath`: an object of type `FilePath` that represents the data's location
  on disk.

## Behavior

### new_dataset

Creates a new [Dataset] value based on the provided inputs.

**Inputs:**
- `url`: dataset's URL
- `checksum`: dataset's checksum for integrity verification
- `filepath`: dataset's file path on disk

**Outputs:** A dataset value. \
**Guarantees:** The returned dataset has an URL that accepts HTTP GET requests,
a valid MD5 checksum string and a file path that exists on disk. 

### fetch

Fetches content from the web using the [Dataset] URL attribute.

**Inputs:** A dataset value. \
**Outputs:** A [Dataframe] value. \
**Requirements:** The [Dataset] attribute is validated. \
**Guarantees:** The [Dataframe] object returned is validated by the dataset's
checksum. If the dataset's file in its URL is compromised in some way, the
function execution fails.

### save

Persists a [Dataframe] to disk using the [Dataset]'s `filepath` attribute. It
saves the dataframe as a Parquet file.

**Inputs:**
- A dataframe `df` to persist to disk
- A dataset providing a path to write `df` to

**Requirements:**
- `df` must exist and be a [Dataframe]
- The [dataset] attribute must contain a `filepath` that exists in local storage

**Guarantees:** There exists a Parquet file at the provided directory containing
the data.

### load

Loads a [Dataframe] from disk using the [Dataset]'s `filepath` attribute. It
loads Parquet files exclusively.

**Inputs:** A dataset. \
**Outputs:** A dataframe. \
**Requirements:** The dataset's `filepath` must exist in storage. \
**Guarantees:** The returned dataframe is not empty.


## See also

[Shared] \
[Modelling methodology]

[Shared]: Shared.md
[Modelling methodology]: ../docs/Methodology.md
[Dataset]: #dataset
[dataset]: #dataset-1
[new]: #new
[fetch]: #fetch
[save]: #save
[load]: #load
[Dataframe]: #dataframe
