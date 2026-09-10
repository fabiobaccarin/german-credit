# Project specification files index

This file provides an entrypoint for the project's specification, listing all
relevant specification files and providing links to them.

## Data service

**File:** [Data.md]

Defines the service responsible for reading, loading and validating data
(including what is sent to and delivered by other services)

## Evaluation service

**File:** [Evaluation.md]

Defines the service responsible for model evaluation and inspection. It
implements methods for scoring models, custom metrics and feature importance
calculators.

## Feature engineering service

**File:** [FeatureEngineering.md]

Defines the service responsible for implementing the feature engineering
strategy defined in the [modelling methodology]. In particular, it provides
the [model service] with a pipeline for processing features prior to being
sent to the model for fitting or prediction.

## Logger service

**File:** [Logger.md]

Defines the service responsible for logging messages in a structured and
persistent manner across the project's services.

## Model service

**File:** [Model.md]

Defines the credit score model service that is responsible for fitting and
prediction.

## Tracking service

**File:** [Tracking.md]

Defines the tracking service responsible for registering experiments in MLFlow.

## See also

[Modelling methodology]

[Data.md]: Data.md
[Evaluation.md]: Evaluation.md
[FeatureEngineering.md]: FeatureEngineering.md
[Logger.md]: Logger.md
[Model.md]: Model.md
[Tracking.md]: Tracking.md
[model service]: #model-service
[Modelling methodology]: ../docs/Methodology.md
