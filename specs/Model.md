# Model service specification

This file describes the public API for the model service.

**Summary:** The model service is implemented as Python class responsible for
fitting models and using them for prediction.

## Signature

**Name:** `ModelService` \
**Description:** Implements model fitting and prediction

## Attributes

### `algorithm`

**Type:** `Algorithm` \
**Description:** One of the options of algorithms to choose from

## Methods

### `new`

**Type:** `classmethod` \
**Description:** Class constructor that validates inputs \
**Inputs:** [algorithm] \
**Outputs:** An object of class `ModelService`

### `fit`

**Type:** `method` \
**Description:** Trains the model \
**Inputs:** A `Dataset` object containing processed inputs \
**Outputs:** A `ClassificationModel` object representing the fitted model and
its metadata \
**Preconditions:** The `Dataset` provided was validated against the data
contract specified in the [Data] layer 

**Postconditions:**
- The outputted `ClassificationModel` has a fitted model inside it
- The outputted `ClassificationModel` has its complete feature list
- The outputted `ClassificationModel` has its pipeline inside it

### `predict`

**Type:** `method` \
**Description:** Uses the model to make predictions on data

**Inputs:**
- A `Dataset` object containing processed inputs
- A `ClassificationModel` object containing the model and its metadata

**Outputs:** A `Predictions` object containing raw and processed predictions

**Preconditions:**
- The `Dataset` provided was validated against the data contract specified in 
    the [Data] layer
- The `ClassificationModel` provided has a fitted model inside it and all
    necessary metadata

## See also

[Data] \
[Domain] \
[Modelling methodology]

[Data]: Data.md
[Domain]: Domain.md
[Modelling methodology]: ../docs/Methodology.md
[algorithm]: #algorithm
