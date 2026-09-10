# Credit score model specification

This file defines the model developed in the project and its implementation in
code.

## Evaluation

**Summary:** The evaluation strategy will be based on the expected credit loss
framework. It will provide 4 metrics to compare models against each other. Two
of them are the total and average costs of the model, which are calculated
based on the estimated probability of default and the corresponding loan amount.
The other two are specifically designed to optimize model training by ensuring
the embedded mathematical optimization problem is convex. These metrics are the
total and the average loss of the model. They replace the probability of default
estimate by a proper scoring rule and process the loan amounts to reduce outlier
influence and improving the smoothness of the loss function topology.

The model will be evaluated using a simplified version of IFRS 9's
[expected credit loss] (ECL) framework. In particular, we define the model's
cost function as follows:

$$
\text{Cost} = \text{Probability of default} \times \text{Loan amount}
$$

Or, more succinctly:

$$
C = \hat{y} \times LA
$$

This is equivalent to assuming that, once the customer defaults, the bank loses
all the lent amount (the loss given default is equal to 100%). It also assumes
that the customers that default always default without having paid anything,
which is a strong assumption. For a more detailed discussion of assumptions,
see the [Assumptions] section.

Therefore, the model's total cost $C^{*}$ will be the sum of the cost across all
customers $i = 1, .., N$:

$$
C^{*} = \sum_{i = 1}^{N}{\left( \hat{y} \times LA \right)}
$$

To be able to experiment with more than one [splitting strategy], we will
normalize the total cost by the number of customers evaluated to get the
*average cost per customer* $\gamma$:

$$
\gamma = \frac{C^{*}}{N}
    = \frac{\sum_{i = 1}^{N}{\left( \hat{y} \times LA \right)}}{N}
$$

Despite being very intuitive for a human, the total cost $C^{*}$ and the
average cost per customer $\gamma$ are not the best choices for a *training*
metric, which we will call a *loss function*. Both the total cost and the
average cost are non-convex against the model's output, which my destabilize
the model training, exposing it to outlier influence our making the model
arrive at local optima. Therefore, we will use a properly convex loss function
$L$ for training, and will report it alongside the total and average costs for 
model evaluation.

This loss function will achieve convexity in 2 ways. First, it will replace the
probability of default (PD) estimate by a proper scoring rule associated with
calibrated probabilities. Second, it will stabilize the loan amount values that
serve as weights in such a way to reduce the influence of extreme values in
the training.

We considered 2 alternatives for a proper PD scoring rule: the [log-loss] and
the [Brier score]. Despite the log-loss being the default choice for PD
modelling, we think the Brier score is a better choice here. First of all,
because the dataset has only 1_000 rows in total, which might make a
log-loss-based loss function particularly susceptible to overfitting because
the log-loss heavily penalizes tail risks. While it would be useful to penalize
tail risks in model training, we think this can be better accomplished by
running stress tests with [value-at-risk] (VaR) estimates. This will make the
risks much more transparent compared to embedding it into the model training.

Second, the Brier score is a quadractic function of the PD, which is
particularly helpful for mathematical optimization. It functions like a [RMSE]
estimate for probabilities, with all the advantages that quadractic functions
bring for convex optimization and gradient stabilization.

Finally, the Brier score also penalizes tail risk, but less heavily. This will
help the model be more robust to outliers, which is our major concern in such
a small dataset. It will help to make the model a best tool by forwarding the
most common cases to automation while letting humans deal with extreme cases
properly. That is, in our view, how the model should behave: we don't want it to
do everything; we want it to handle the straightforward cases so that we can
focus on what matters most for the business. A reliable plain model is much
better than an unreliable sophisticated one.

The other part of the loss-function is the loan amount processing. Instead of
using the loan amount values directly as weights, we will replace them by their
square roots. Because loan amounts are necessarily non-negative and the square
root is a monotonic continuous function, there is no loss of generality in using
the square root of the loan amounts instead of raw values. We get the advantage
of reducing the influence of large loans in the loss function and its smoothing
at the cost of a small tail risk error that can be compensated with stress
tests.

We also considered using the natural logarithm instead of the square root. We
rejected this course of action because of 2 problems. First, the logarithm goes
to negative infinity as it approaches zero, which will result in unstable
weights for comparatively small loans. Second, the logarithm will take tail
risks too lightly. Given that the square root already gives the stabilization
and mathematical convexity we need, there is no reason to incur the extra tail
risk costs that the natural logarithm brings to the modelling.

Therefore, our loss function $L$ can be defined as follows:

$$
L = {\left( \hat{y} - p \right)}^{2} \times \sqrt{LA}
$$

With its total and average values $L^{*}$ and $\lambda$ defined as:

$$
L^{*} = \sum_{i = 1}^{N}{
    \left[ {\left( \hat{y} - p \right)}^{2} \times \sqrt{LA} \right]
}
$$

$$
\lambda = \frac{L^{*}}{N}
$$

## Splitting strategy

The dataset will be split in a 80/20 fashion: 80% of the dataset will be used
to train the model and the remaining 20% will be used to test its generalization
capabilities and fairness. We will explore other splittings such as 70/30, 60/40
and 50/50 to understand how the model behaves.

## Assumptions

We make 2 important assumptions about our problem:

1. **Loans are entirely lost upon default.** By not including the loss given
   default in our evaluation metrics, we effectively say that we lose everything
   upon default. This is equivalent to say that the bank does not have an
   effective credit recovery strategy. It is a strong assumption that heavily
   penalizes the final ECL estimates, but that will be addressed by scenario
   analysis. Our focus here is PD modelling to reduce worst-case scenario
   exposure, so this assumption provides necessary simplification of the
   problem.
2. **Customers default without paying anything.** Because we are using the total
   initial loan amount as exposure for our ECL calculations, we are ignoring all
   intermediate paymentss a customer makes prior to defaulting. This is also a
   strong assumption. However, it highlights the credit granting dimension of
   the problem: by emphasizing the initial loan values, we penalize credit
   decisions that gave large loans to bad customers from the start, irrespective
   if they had paid some part of the loans prior to defaulting. This is an
   approach focused on not letting bad customers enter the portfolio in the
   first place, instead of having them enter and then figure out a way to
   recover from their default. We think this is what a credit rating model
   should do, while the credit policy itself should be responsible to make room
   for commercial goals. It is much easier to tighten or loosen a credit policy
   rule than to make a new credit scoring model to play along new commercial
   strategies.

## Implementation

The model will be implemented as a Python class that knows how to process
features for the model, fit the model and make predictions with new data. It
will also generate logs for auditability of its behavior.

### Pseudocode

```
CLASS Model:
    METHOD __init__:
        INPUTS: None
        OUTPUTS: An object of CLASS Model
        PURPOSE: Class constructor
        SIDE EFFECTS: Allocates memory to hold an object of CLASS Model
CLASS ModelInterface
    """
    Implements model fitting API
    """

    METHOD __init__
        INPUTS
            _validated: an object of validated information to store inside the
            object
        OUTPUTS
            An object of CLASS ModelInterface
        DESCRIPTION
            Instantiates an object of the CLASS ModelInterfacee
        SIDE EFFECTS
            None
        PRECONDITIONS
            _validated.features must not be empty
            AND _validated.algorithm must be one among a finite set of 
                possibilities
            AND _validated.data_interface must not be empty and must be of the 
                required type
            AND _validated.evaluation_interface must not be empty and must be
                of the required type
            AND _validated.feature_engineering_interface must not be empty and 
                must be of the required type
            AND _validated.logger must not be empty and must be of the required 
                type
        POSTCONDITIONS
            self.features exists
            AND self.algorithm exists as an object implemeting the algorithm
            AND self.data_interface exists
            AND self.evaluation_interface exists
            AND self.feature_engineering_interface exists
            AND self.logger exists
            AND self._is_fitted is False
    END

    CLASSMETHOD new
        INPUTS
            features: list of strings containing feature names
            algorithm: a string naming one of a set of finite algorithm options
            data_interface: an object of CLASS DataInterface
            evaluation_interface: an object of CLASS EvaluationInterface
            feature_engineering_interface: an object of
                CLASS FeatureEngineeringInterface
        OUTPUTS
            An object of CLASS ModelInterface
        DESCRIPTION
            Class constructor
        PRECONDITIONS
            None
        POSTCONDITIONS
            features must not be empty
            AND algorithm must be one among a finite set of possibilities
            AND data_interface must not be empty and must be of the required
                type
            AND evaluation_interface must not be empty and must be of the
                required type
            AND logger must not be empty and must be of the required type
    END
    
    METHOD _fit
        INPUTS
            data: Data in tabular form
        OUTPUTS
            An object of CLASS ModelInterface
        DESCRIPTION
            Fits the model according to the evaluation interface
        SIDE EFFECTS
            Modifies the object of CLASS ModelInterface to hold the fitted 
            algorithm with its metadata and evaluation metrics
        PRECONDITIONS
            self.algorithm exists
            AND data obeys the data contract established by the
                self.data_interface
        POSTCONDITIONS
            self.algorithm is fitted
            AND self.evaluation_interface.metrics is not empty
    END

    METHOD fit
        INPUTS
            data: Data in tabular form
        OUTPUTS
            An object of CLASS Model
        DESCRIPTION
            Wraps the fitting routine around validation rules
        SIDE EFFECTS
            None
        PRECONDITIONS
            None
        POSTCONDITIONS
            self.algorithm exists
            AND data obeys the data contract established by the
                self.data_interface
    END
    
    GETTER METHOD get_is_fitted
        INPUTS
            None
        OUTPUTS
            Boolean: True if self.algorithm is fitted
        DESCRIPTION
            Getter method to check whether the model is fitted
        SIDE EFFECTS
            None
        PRECONDITIONS
            None
        POSTCONDITIONS
            None
    END

    SETTER METHOD set_is_fitted
        INPUTS
            flag: a boolean value
        OUTPUTS
            An object of CLASS ModelInterface
        DESCRIPTION
            Sets the object's attribute self.is_fitted = flag
        SIDE EFFECTS
            None
        PRECONDITIONS
            None
        POSTCONDITIONS
            self._is_fitted is either True or False
    END

    METHOD _predict
        INPUTS
            data: data in tabular form
        OUTPUTS
            predictions: a list of raw predictions
        DESCRIPTION
            Uses the self.algorithm to make predictions in its native format
        PRECONDITIONS
            self.algorithm is fitted
            AND data obeys the data contract established by the
                self.data_interface
        POSTCONDITIONS
            self._raw_predictions exists and conforms to the raw prediction's
            contract established by the data_interface
    END

    METHOD predict
        INPUTS
            data: Data in tabular form
        OUTPUTS
            raw_predictions: A list of predictions in self.algorithm's native
            form
        DESCRIPTION
            Uses the model's underlying algorithm to make predictions
        PRECONDITIONS
            self.algorithm exists
            AND self.algorithm is fitted
        POSTCONDITIONS
            self._raw_predictions exists
    END

    GETTER METHOD get_predictions
        INPUTS
            None
        OUTPUTS
            predictions: List of prediction values processed for decision making
        DESCRIPTION
            Processes raw predictions into a standardized format for decision
            making by the bank
        PRECONDITIONS
            self._raw_predictions exists
        POSTCONDITIONS
            None
    END

    SETTER METHOD set_predictions
        INPUTS
            raw_predictions: List of raw prediction values
        OUTPUTS
            An object of CLASS ModelInterface
        DESCRIPTION
            Sets the interface's attribute self._raw_predictions
        PRECONDITIONS
            raw_predictions exists
            AND raw_predictions is composed of finite numbers
    END
END
```
[expected credit loss]: https://primaconsulting.org/ecl-model-ifrs-9-examples/
[Assumptions]: #assumptions
[splitting strategy]: #splitting-strategy
[log-loss]: https://en.wikipedia.org/wiki/Cross-entropy
[Brier score]: https://en.wikipedia.org/wiki/Brier_score
[value-at-risk]: https://en.wikipedia.org/wiki/Value_at_risk
[RMSE]: https://en.wikipedia.org/wiki/Root_mean_square_deviation
