# Feature engineering service specification

This file describes the public API for feature engineering in the project.

**Summary:** The service is implemented as Python class that is responsible
for generating a Scikit-Learn Pipeline object implementing all the steps
required to produce features for the model.

## Signature

**Name:** `FeatureEngineeringService` \
**Description:** Implements the feature engineering pipeline for the model

## Attributes

### `features`

**Type:** `FeatureList` \
**Description:** List of feature names to process

### `features_to_create`

**Type:** `FeatureFlagMapping` \
**Description:** A mapping of feature names to boolean flags telling the service
which features to create. Each feature must have a dedicated method in the 
service for its creation

## Methods

### `new`

**Type:** `classmethod` \
**Description:** Class constructor that validates inputs \
**Inputs:** [features]; [features_to_create] \
**Outputs:** An object of class `FeatureEngineeringService`

**Postconditions:**
- [features] is not empty and is of required type
- [features_to_create] is not empty and is of required type
- Every key in [features_to_create] has a `_make_feature_<key>` method 
    implemented

### `get_features`

**Type:** `getter` \
**Description:** Returns the complete list of features to pass to the model \
**Outputs:** a `FeatureList` object of feature names

**Preconditions:**
- [features] validated
- [features_to_create] validated

**Postconditions:** the output's length is the sum of [features]'s length and
[features_to_create] keys' length

### `pipeline`

**Type:** `getter`
**Description:** Returns a `Pipeline` object implementing the feature
engineering steps required

**Preconditions:**
- [features] validated
- [features_to_create] validated

## See also

[Domain] \
[Modelling methodology]

[Domain]: Domain.md
[Modelling methodology]: ../docs/Methodology.md
[features]: #features
[features_to_create]: #features_to_create