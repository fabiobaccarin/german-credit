# Project hypotheses

This file lists and explains each hypothesis made about the data or the problem
contained in this project.

## Refusal of customers with no checking account

Customers for which `checking_status == 'no checking'` should be promptly
refused by the bank for loans. They present a significant credit risk to the
bank and absence of paying information because we can't see their checking
account movements. Their credit behavior is opaque to us. We should exclude
them from the model.

**Status:** Pending

## Refusal of customers with delinquency history

Customers for which `credit_history == 'delayed previously'` must be promptly
refused by the bank for loans. They have already shown bad credit behavior and
thus there is little to gain from giving them a second chance. Their risk
outweights their reward.

**Status:** Pending

## Credit for consumption

Customer wanting money for consumption should have higher risk of default
because the money goes to a sink rather than to something that is expected to
generate a future cash flow to help pay the loan back.

**Status:** Pending

## Gender irrelevance

There is no relevant credit risk difference between males and females.

**Status:** Pending

## Marital status irrelevance

There is no relevant credit risk difference between different marital stata.

**Status:** Pending

## Model fairness

The model treats customers equally irrespective of their gender, marital status
or other demographic groupings.

**Status:** Pending