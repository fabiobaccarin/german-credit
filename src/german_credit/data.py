"""Read, write, and validate the German credit dataset."""

import hashlib
import io
from pathlib import Path
from typing import Annotated
from urllib.request import Request, urlopen

import polars as pl
from polars import DataFrame
from pydantic import BaseModel, ConfigDict, Field, FilePath, HttpUrl

type MD5ChecksumString = Annotated[str, Field(pattern=r"^[0-9a-fA-F]{32}$")]
type Dataframe = DataFrame


class Dataset(BaseModel):
    """Immutable metadata describing a dataset"""

    model_config = ConfigDict(frozen=True)

    url: HttpUrl | None = None
    checksum: MD5ChecksumString | None = None
    filepath: FilePath

    @property
    def get_filepath(self) -> Path:
        """Return the path to the dataset on disk"""
        return Path(self.filepath)


def _get(url: HttpUrl) -> bytes:
    """Fetch URL content and fail for non-successful HTTP responses."""
    request = Request(str(url), method="GET")
    with urlopen(request) as response:
        status = getattr(response, "status")
        if not 200 <= status < 300:
            raise RuntimeError(f"GET {url} returned HTTP status {status}")
        return response.read()


def _validate_checksum(
    *, content: bytes, checksum: MD5ChecksumString | None
) -> None:
    if checksum is not None:
        actual = hashlib.md5(content).hexdigest()
        if actual.casefold() != checksum.casefold():
            raise ValueError(
                f"Dataset checksum mismatch: expected {checksum}, got {actual}."
            )


def new_dataset(
    *,
    filepath: FilePath,
    url: HttpUrl | None = None,
    checksum: MD5ChecksumString | None = None,
) -> Dataset:
    """Create a validated dataset value"""
    dataset = Dataset(url=url, checksum=checksum, filepath=filepath)
    return dataset


def fetch(dataset: Dataset) -> Dataframe:
    """Fetch and checksum-validate a remote dataset as a Polars dataframe."""
    if not isinstance(dataset, Dataset):
        raise TypeError("dataset must be a Dataset.")
    if dataset.url is None:
        raise ValueError("A dataset URL is required to fetch data.")

    content = _get(dataset.url)
    _validate_checksum(content=content, checksum=dataset.checksum)
    dataframe = pl.read_parquet(io.BytesIO(content))
    if dataframe.is_empty():
        raise ValueError("Fetched dataset is empty.")
    return dataframe


def save(*, df: Dataframe, dataset: Dataset) -> None:
    """Persist a Polars dataframe as a Parquet file."""
    if not isinstance(df, pl.DataFrame):
        raise TypeError("df must be a Polars DataFrame.")
    if not isinstance(dataset, Dataset):
        raise TypeError("dataset must be a Dataset.")
    df.write_parquet(dataset.get_filepath)


def load(dataset: Dataset) -> Dataframe:
    """Load a non-empty Polars dataframe from a dataset's Parquet file."""
    if not isinstance(dataset, Dataset):
        raise TypeError("dataset must be a Dataset.")
    dataframe = pl.read_parquet(dataset.filepath)
    if dataframe.is_empty():
        raise ValueError("Dataset is empty.")
    return dataframe


def _fetch_and_save() -> None:
    """Fetches data and saves it. Meant to be run as a project script"""
