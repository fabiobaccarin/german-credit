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

## Module: model

**File:** `src/german_credit/model.py`

The `model` module implements domain models and functionality relating to
machine learning models. The most important domain model is `Model`, which
validates and stores information relating to the model, like list of features,
preprocessing steps, training and testing logic, etc.

With a `Model` object, the user can perform actions on it, like `preprocess`,
`get_features`, `train`, `test`, `predict`, `evaluate` and `dump`.

Example:

```python
from german_credit import model

model_spec = model.Model(
    name="foo",
    features=["foo", "bar"],
    preprocessor=some_sklearn_pipeline_object,
    predictor="logistic-regression",
    file="path-to-pickle.joblib"
)

fitted_model = model.train(model_spec)
model.dump(fitted_model, model_spec)

metrics = model.evaluate(model_spec)
```
