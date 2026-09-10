# Domain specification

This file describes the domain models used to represent data and business
entities across the project.

**Summary:** The domain models are implemented as Pydantic models that
implement restrictions or serve as mechanisms to avoid primitive obsession. Many
models act as aggregation layers for related data.

## `URL`

A non-empty string representing an URL.

## `MD5ChecksumString`

A non-empty string representing a MD5 string.

## `FeatureName`

A non-empty string representing a feature name.

## `Dataframe`

An alias for a Polars Dataframe.

## `ClassificationModel`

An union type for `LogisticRegression`, `LinearSVC`, `RandomForestClassifier`, 
`DecisionTreeClassifier` and `XGBClassifier`.

## `FeatureList`

A non-empty list of [FeatureName] values.

## `FeatureImportance`

An alias for Pydantic's `NonNegativeFloat`.

## `FeatureImportanceMapping`

A mapping of [FeatureName] values to [FeatureImportance] values in a 1-to-1
relationship.

## `Metric`

An union type for `'average_customer_cost'` and `'average_customer_loss'`.

## `ModelScore`

An alias for [NonNegativeFloat].

## `ModelScoreMapping`

A mapping of [Metric] values to [ModelScore] values in a 1-to-1 relationship.

## `Dataset`

Immutable container object representing a dataset.

### `url`

A [URL] value identifying the dataset's parquet file location on the OpenML 
server. It must accept a HTTP GET request.

### `checksum`

A [MD5ChecksumString] value containing the dataset's checksum for integrity
verification.

### `content`

A [DataFrame] value representing the dataset's information.

## `Model`

Immutable container object representing a fitted model and its metadata.

### `engine`

A [ClassificationModel] value representing the fitted credit score model.

### `features`

A [FeatureList] value representing the list of features' names used by the
model.

### `pipeline`

A Sci-kit Learn pipeline value representing the feature engineering pipeline used 
to process information prior to sending it to the model.

### `importances`

A [FeatureImportanceMapping] value mapping each value in [features] to a 
[FeatureImportance] value.

### `scores`

A [ModelScoreMapping] value mapping each [Metric] value to a [ModelScore] value.

[URL]: #url
[MD5ChecksumString]: #md5checksumstring
[Dataframe]: #dataframe
[ClassificationModel]: #classificationmodel
[FeatureList]: #featurelist
[Pipeline]: #pipeline
[features]: #features
[FeatureImportance]: #featureimportance
[FeatureImportances]: #featureimportances
[FeatureName]: #featurename
[FeatureImportanceMapping]: #featureimportancemapping
[Metric]: #metric
[ModelScore]: #modelscore
[ModelScoreMapping]: #modelscoremapping
