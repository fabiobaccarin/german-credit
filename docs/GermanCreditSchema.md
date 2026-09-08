# Dataset dictionary for German Credit dataset

This file provides column-wise metadata for each column in the project's
dataset. All information is extracted from the [GermanCreditCroissant.json]
file, but organized in a way to facilitate consultation by humans and
complemented with outside information when needed.

## Checking status

**Name:** checking_status

**Description:** Each value describes the state of the customer's checking
account at the time of measurement.

**Type:** Categorical

**Possible values:** The numbers represent values in Deutsche Marks
* `"<0"`
* `"0<=X<=200"`
* `">=200"`
* `"no checking"`

## Credit history

**Name:** `credit_history`

**Description:** Each value describes the customer's credit history
qualitatively.

**Type:** Categorical

**Possible values:**
* `"all paid"`: indicates a customer that has paid all loans with the bank
* `"critical/other existing credit"`: indicates critical accounts holding debts
  with other banks (possible business opportunity)
* `"delayed previously"`: the customer has default history
* `"existing paid"`: the customer has loans outstanding but is paying them
* `"no credits/all paid"`: customers that have no credit history with the bank

## Purpose of the loan

**Name:** `purpose`

**Description:** What the customer will do with the loan

**Type:** Categorical

**Possible values**:
* `"business"`
* `"domestic appliance"`
* `"education"`
* `"furniture/equipment"`
* `"new car"`
* `"other"`
* `"radio/tv"`
* `"repairs"`
* `"retraining"`
* `"used car"`
* `"vacation"`

## Credit for consumption

**Name:** `is_credit_for_consumption`

**Description:** Derived from the [loan's purpose column], this column has the
value `yes` if the loan's purpose is one of these values:
* `"domestic appliance"`
* `"new car"`
* `"other"`
* `"radio/tv"`
* `"used car"`
* `"vacation"`

Otherwise, the value is `no`. See the [credit for consumption hypothesis].

**Type:** String/Boolean

## Saving status

**Name:** `saving_status`

**Description:** Each value describes the amount a customer has in their
savings account, in Deutsche Marks.

**Type:** Categorical

**Possible values**:
* `"100<=X<500"`
* `"500<=X<1000"`
* `"<100"`
* `">=1000"`
* `"no known savings"`

## Years employed

**Name:** `employment`

**Description:** The number of years that the customer has the current job

**Type:** Categorical

**Possible values:**
* `"<1"`
* `"1<=X<4"`
* `"4<=X<7"`
* `">=7"`
* `"unemployed"`

## Gender and marital status

**Name:** `personal_status`

**Description:** The combination of the customer's gender and marital status.
It is against current regulations to use this information for credit risk
analysis unless there is compelling evidence of their relevance to the problem.
We demonstrate the lack of such evidence in our [gender irrelevance hypothesis]
and in our [marital status irrelevance hypothesis]. However, the column will
be used to evalute the final model's fairness across different gender and
demographic groups.

**Type:** Categorical

**Possible values:**
* `"female div/dep/mar"`
* `"female single"`
* `"male div/sep"`
* `"male mar/wid"`
* `"male single"`

## Gender

**Name:** `gender`

**Description:** Derived from the [gender and marital status column]. This 
column isolates the gender from the marital status to be able to gauge how
the model performs across genders.

**Type:** String/Boolean

**Possible values:**
* `"male"`
* `"female"`

## Marital status

[GermanCreditCroissant.json]: GermanCreditCroissant.json
[loan's purpose column]: #purpose-of-the-loan
[credit for consumption hypothesis]: Hypotheses.md
[gender irrelevance hypothesis]: Hypotheses.md
[marital status irrelevance hypothesis]: Hypotheses.md
