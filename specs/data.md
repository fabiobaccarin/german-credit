# Data module specification

This file describes the domain models and functionalities in detail. The module
is responsible for handling data reading, writing and validation in the project.

## Domain models

- [Dataset]
- [MD5ChecksumString]
- [Dataframe]

### Domain model: `MD5ChecksumString`

`MD5ChecksumString` is a string with proper validation rules relating to MD5
hash generation.

### Domain model: `Dataframe`

An alias for a Polars DataFrame object.

### Domain model: `Dataset`

`Dataset` is a Pydantic model representing a dataset in our project. This model
is responsible for ensuring that all actions performed on data are taken with
validated data.

#### Dataset: fields

- **`content_url`:** a Pydantic `HttpUrl` pointing to the file's location on the
  internet. The URL must accept a HTTP GET request. \
- **`md5`:** a [MD5ChecksumString] that represents the dataset's MD5 validation
  value. It is used to check the file's integrity when reading data from the
  internet or from disk. \
- **`file`:** a Pydantic `FilePath` to local storage where to write to (or read 
  from) disk. It must have a `.parquet` extension.

## Actions 

- [read]
- [write]

### Action: read

`read` receives a `Dataset` as input and returns a `DataFrame` as output,
handling the checksum validation to confirm integrity. It first tries to reach
for local storage; if the file is not found, then it tries to fetch it from the
url provided.

### Action: write

`write` receives a `Dataframe` and a `Dataset` and writes the `Dataframe` to
local storage designed by the `Dataset` file path.

[Dataframe]: #domain-model-dataframe
[Dataset]: #domain-model-dataset
[MD5ChecksumString]: #domain-model-md5checksumstring
[read]: #action-read
