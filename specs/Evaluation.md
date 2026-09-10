# Evaluation service specification

This file describes the evaluation service specification for the project. For
brevity, the `__init__` method is omitted. If entries like **Inputs**,
**Preconditions** or **Postconditions** are omitted, it is assumed that they 
aren't applicable to the method. Only the public API is specified.

**Summary:** The evaluation layer is implemented as a Python class responsible
for model scoring and inspection. Objects of the class must be instantiated by
calling the `new` method. Its inputs are a list of feature names and the number
of permutations to execute for feature importance. The class exposes getter
method for retrieving the average metrics per customer.

## Signature

**Name:** `EvaluationService` \
**Description:** Implements the evaluation strategy for the project

## Attributes

### `features`

**Type:** `FeatureList` \
**Description:** List of feature names to evaluate for model inspection

### `permutations`

**Type:** `PositiveInteger` \
**Description:** Number of permutations to execute

### `customer_costs`

**Type:** `NonNegativeFloatArray` \
**Description:** Collection of `NonNegativeFloat` values representing customer 
costs

### `customer_losses`

**Type:** `NonNegativeFloatArray` \
**Description:** Collection of `NonNegativeFloat` values representing customer
losses

## Methods

### `new`

**Type:** `classmethod` \
**Description:** Class constructor that validates inputs \
**Inputs:** [features]; [permutations] \
**Outputs:** An object of class `EvaluationService`

**Postconditions:**
- `features` is not empty and is of required type
- `permutations` is a positive integer

### `importances`

**Type:** `getter` \
**Description:** Feature importances \
**Outputs:** a `FeatureImportances` object containing the feature importance
estimate for each feature in [features]

**Preconditions:**
- [features] exists and is of required type
- [permutations] exists and is of required type

**Postconditions:**
- Every value in `results` is of type `FiniteFloat`
- Every feature in [features] has a key in `results`

### `average_customer_cost`

**Type:** `getter` \
**Description:** Average cost per customer \
**Outputs:** a `NonNegativeFloat` representing the average cost per customer \
**Preconditions:** [customer_costs] exists and is of required type \
**Postconditions:** the output is a `NonNegativeFloat`

### `average_customer_loss`

**Type:** `getter` \
**Description:** Average loss per customer \
**Outputs:** a `NonNegativeFloat` representing the average loss per customer \
**Preconditions:** [customer_losses] exists and is of required type \
**Postconditions:** the output is a `NonNegativeFloat`

## See also

[Domain] \
[Modelling methodology]

[Modelling methodology]: ../docs/Methodology.md
[Domain]: Domain.md
[features]: #features
[permutations]: #permutations
[customer_costs]: #customer_costs
[customer_losses]: #customer_losses
