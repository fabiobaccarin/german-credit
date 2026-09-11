from __future__ import annotations

from typing import Annotated, Literal, TypeAlias

import polars as pl
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FilePath,
    HttpUrl,
    NonNegativeFloat,
    StringConstraints,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

URL: TypeAlias = HttpUrl

MD5ChecksumString: TypeAlias = Annotated[
    str,
    StringConstraints(
        pattern=r"^[A-Fa-f0-9]{32}$", min_length=32, max_length=32
    ),
]

FeatureName: TypeAlias = Annotated[str, StringConstraints(min_length=1)]
Dataframe: TypeAlias = pl.DataFrame

ClassificationModel: TypeAlias = (
    LogisticRegression
    | LinearSVC
    | RandomForestClassifier
    | DecisionTreeClassifier
    | XGBClassifier
)


FeatureList: TypeAlias = Annotated[list[FeatureName], Field(min_length=1)]
FeatureImportance: TypeAlias = NonNegativeFloat
FeatureImportanceMapping: TypeAlias = dict[FeatureName, FeatureImportance]

Metric: TypeAlias = Literal["average_customer_cost", "average_customer_loss"]
ModelScore: TypeAlias = NonNegativeFloat
ModelScoreMapping: TypeAlias = dict[Metric, ModelScore]


class Dataset(BaseModel):
    """Immutable container object representing a dataset."""

    model_config = ConfigDict(frozen=True)

    url: URL
    checksum: MD5ChecksumString
    file_path: FilePath


class Model(BaseModel):
    """Immutable container object representing a fitted model and metadata."""

    model_config = ConfigDict(frozen=True)

    engine: ClassificationModel
    features: FeatureList
    pipeline: Pipeline
    importances: FeatureImportanceMapping
    scores: ModelScoreMapping


__all__ = [
    "URL",
    "MD5ChecksumString",
    "FeatureName",
    "Dataframe",
    "ClassificationModel",
    "FeatureList",
    "FeatureImportance",
    "FeatureImportanceMapping",
    "Metric",
    "ModelScore",
    "ModelScoreMapping",
    "Dataset",
    "Model",
]
