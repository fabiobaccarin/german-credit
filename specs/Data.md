# Data service specification

This file describes the project's data service public API.

**Summary:** The data service is implemented as a Python class responsible for
reading, writing and validating data.

## Signature

**Name:** `DataService` \
**Description:** Implements data reading, writing and validation

## Attributes

### `dataset`

**Type:** `Dataset` \
**Description:** Container storing the dataset's URL, its destination file and
its checksum

### `model_schema`

**Type:** `ModelSchema` \
**Description:** Container storing the data contract regarding the model's
inputs

### `prediction_schema`

**Type:** `PredictionSchema` \
**Description:** Container storing the data contract regarding the model's
predictions

## Methods

### `new`

**Type:** `classmethod` \
**Description:** Class constructor that validates inputs \
**Inputs:** [content]; [model_schema]; [prediction_schema] \
**Outputs:** An object of class `DataService`

### `fetch`

**Type:** `method` \
**Description:** Retrieves data based on its [content]'s URL \
**Outputs:** A `Dataset` object with the data and metadata

**Preconditions:**
- The [content]'s URL exists and accepts HTTP GET requests
- The [content]'s checksum is a valid checksum string

**Postconditions:**
- The `Dataset` returned is not empty and has file integrity

### `save`

**Type:** `method` \
**Description:** Write a `Dataset`'s content to disk as a Parquet file \

**Inputs:**
- A `FilePath` object containing the address on disk to write
- A `Dataset` to write to disk

**Preconditions:**
- The `FilePath` must exist in disk and must be writable
- The `Dataset` must not be empty

**Postconditions:**
- A Parquet file exists on disk in the specified location

### `load`

**Type:** `method` \
**Description:** Loads a Parquet file from disk into a `Dataset` \
**Inputs:** A `FilePath` address to the file \
**Outputs:** A `Dataset` based on the `FilePath` provided \
**Preconditions:** The `FilePath` must exist on disk and be readable \
**Postconditions:** The `Dataset` is not empty

### `load_model`

**Type:** `method` \
**Description:** Loads a `Model` from disk \
**Inputs:** A `FilePath` address to the file in which the model is stored \
**Outputs:** A `Model` with all its attributes \
**Preconditions:** The `FilePath` must exist on disk and be readable \
**Postconditions:** The loaded `Model` must have all its attributes

### `dump`

**Type:** `method` \
**Description:** Writes a `Model` to disk as a pickle file

**Inputs:**
- A `FilePath` address to the file to write
- A `Model` to write to disk

**Preconditions:**
- The provided `FilePath` must be writable and exist on disk
- The provided `Model` must be fitted

**Postconditions:** There exists a file at `FilePath` containing the `Model`'s 
data and its attributes

## See also

[Domain] \
[Modelling methodology]

[Domain]: Domain.md
[Modelling methodology]: ../docs/Methodology.md
[content]: #content
[model_schema]: #model_schema
[prediction_schema]: #prediction_schema
