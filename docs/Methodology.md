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
influence and improving the smoothness of the loss function topology. Model
inspection will be implemented through permutation importance estimates for the
average customer cost to keep model inspection robust, easy to explain and
insighful for the business problem.

### Metrics

The model will be evaluated using a simplified version of IFRS 9's ECL
([expected credit loss]) framework. In particular, we define the model's
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
PD (probability of default) estimate by a proper scoring rule associated with
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
running stress tests with VaR ([value-at-risk]) estimates. This will make the
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

### Model inspection

Regarding model inspection, we will implement [permutation importance] estimates
based on bootstrapping the average cost per customer. This will ensure that
every model we make is inspectionable in a way that is meaningful both to
data scientists and business professionals.

## Splitting strategy

The dataset will be split in a 80/20 fashion: 80% of the dataset will be used
to train the model and the remaining 20% will be used to test its generalization
capabilities and fairness. We will explore other splittings such as 70/30, 60/40
and 50/50 to understand how the model behaves.

## Feature engineering

The major concern for feature engineering is the dataset size. Given that we
only have at most 800 lines of data to train our model, it is paramount to keep
the dimensionality of the feature space as small as possible. To do that, we
considered 2 alternatives: smoothed target encoding and GLMM (generalized linear 
mixed model) encoding[¹].

Smoothed target encoding and GLMM encoding are fundamentally the same thing. The
difference lies in that GLMM is a more statistically principled way to
implement regularized target encoding. Instead of blending local and global
average as in smoothed target encoding, GLMM encoding estimates a random
effects model. This has the advantage of enabling sharing of information between
rows, thus being much more robust to overfitting. GLMMs assume all observations
come from the same underlying (Gaussian) distribution with 0 mean and an unknown
variance. The GLMM's job is simply to estimate this variance to estimate the
random effects.

The GLMM model works similarly to a dummy model, but with important differences.
Random effects are like dummies on steroids: instead of estimating statical
local coefficients (which are fixed effects), random effects estimate an entire
distribution to understand subpopulation behavior. Random effects can be
understood as a regularized version of dummy variables, where regularization
is implemented hierarchically through variance shrinkage towards 0 mean.

In practice, this means we get an output very similar to smoothed target
encoding, but within a more robust regularization framework than simple average
blending. For small datasets (as is our case), this is ideal. For large
datasets, GLMMs are computationally expensive. Also, we have enough data to make 
simple average blending effective in controlling overfitting, so smoothed target
encoding is more appropriate.

At the end of feature engineering, every categorical feature will be encoded as
a single numeric column. Then, we will standardize all features to have 0 mean
and unit variance. We don't have missing data in our dataset, but we will train
simple imputers anyway to make the model robust in production. The fact that we
don't have missing data in our dataset does not guarantee we won't have missing
data in production, so it is good to be prepared for this scenario.

This will, however, make the model fail silently in production. We understand
that this is a feature, not a bug. The model's job is to make reliable
predictions of credit risk, not monitor data quality. Missing values prevalence
must be monitored separately inside data quality monitoring processes.
Decoupling these things (data quality and model prediction) imply that not all
missing data represent a problem: if we have 1% of missing data, that is not
likely an issue.

## Assumptions

We make 4 important assumptions about our problem:

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
3. **Categorical effects come from the same distribution.** This is the main
   assumption we make to implement our [Feature engineering] strategy. This
   assumption is not necessarily unrealistic: customers with different kinds of
   jobs or checking account stata may come from the same underlying risk
   distributions. There is no reason to believe the risk distribution for
   customers with less than 1 year at a job is fundamentally different from the
   risk distribution for customers with more than 7 years at a job. It seems
   quite reasonable to assume that both kinds of customers come from the same
   distribution, but from different places inside it. Even if this weren't true,
   we wouldn't have enough data to estimate a different distribution for all
   subgroups in the data. So we don't have a choice but to make some simplifying
   distributional assumption. This seems the least restrictive of our options.
4. **Single responsibility principle.** There are 2 main components to our
   project: data and modelling. We assume each component must work independently
   of the other and do only 1 thing realy well. This implies that our model's
   responsibility is to make reliable predictions, not to ensure its inputs are
   correct. Similarly, our data interface's job is to ensure the model's input
   are correct, not to make reliable predictions based on them. In practice,
   this means our model will have imputers in place to handle missing data even
   if we don't have any missing data in our dataset. The model won't halt
   execution upon receiving missing data. To monitor missing data is our data
   interface's job.

## Implementation

The model will be implemented as a Python class that knows how to process
features for the model, fit the model and make predictions with new data. It
will also generate logs for auditability of its behavior.

### Pseudocode

```
CLASS EvaluationInterface
    """
    Implements model evaluation API. Its responsibility is to score and explain
    the model.
    """

    METHOD __init__
        INPUTS
            _validated: an object of validated information to store inside the
            object
        OUTPUTS
            An object of CLASS EvaluationInterface
        DESCRIPTION
            Instantiates an object of CLASS EvaluationInterface
        SIDE EFFECTS
            Logs object creation
        PRECONDITIONS
            _validated.features must not be empty and must be of required type
            AND _validated.permutations must not be empty and must of required
                type
        POSTCONDITIONS
            self.features exists
            self.permutations exists
    END

    CLASS METHOD new
        INPUTS
            features: list of strings representing feature names
            permutations: number of permutations to perform for each feature
        OUTPUTS
            An object of CLASS EvaluationInterface
        SIDE EFFECTS
            None
        PRECONDITIONS
            None
        POSTCONDITIONS
            features must not be empty and must be of required type
            AND permutations must not be empty and must of required type
    END

    GETTER METHOD importances
        INPUTS
            None
        OUTPUTS
            values: a list of importance estimates for each feature in
                self.features
        DESCRIPTION
            Calculates feature importances
        SIDE EFFECTS
            Logs feature importances
        PRECONDITIONS
            self.features exists
            AND self.permutations exists
        POSTCONDITIONS
            Every value in values is a non-finite number and every feature in
            self.features has an associated value
    END

    STATIC METHOD _check_pd
        INPUTS
            pd: customer's estimated PD
        OUTPUTS
            None
        DESCRIPTION
            Implements preconditions for PD usage in calculations
        SIDE EFFECTS
            Halts program execution upon failure and logs error
        PRECONDITIONS
            None
        POSTCONDITIONS
            pd is in the interval (0, 1)
    END

    STATIC METHOD _check_loan_amount
        INPUTS
            loan_amount: customer's loan amount in Deutsche Marks
        OUTPUTS
            None
        DESCRIPTION
            Implements preconditions for loan amount usage in calculations
        SIDE EFFECTS
            Halts program execution upon failure and logs error
        PRECONDITIONS
            None
        POSTCONDITIONS
            loan_amount is a non-negative real number
    END
    
    METHOD _check_customer_cost_inputs
        INPUTS
            probability_default: customer's estimated PD
            AND loan_amount: customer's approved loan amount
        OUTPUTS
            None
        DESCRIPTION
            Checks preconditions for calculating the customer's cost
        SIDE EFFECTS
            None
        PRECONDITIONS
            None
        POSTCONDITIONS
            probability_default is in the (0, 1) interval
            AND loan_amount is a non-negative real number
    END

    METHOD _generalized_loss_function
        INPUTS
            pd: PD estimate
            AND loan_amount: customer's approved loan amount
            AND calculate_brier: flag to indicate whether the Brier score should
                be calculated
        OUTPUTS
            results: a list of non-negative real numbers
        DESCRIPTION
            Calculates the loss or cost functions
        SIDE EFFECTS
            None
        PRECONDITIONS
            probability_default is in the (0, 1) interval
            AND loan_amount is a non-negative real number
            AND calculate_brier must be either True or False
        POSTCONDITIONS
            results is a list of non-negative real numbers
    END

    METHOD _calculate_customer_cost
        INPUTS
            probability_default: customer's estimated PD
            AND loan_amount: customer's approved loan amount
        OUTPUTS
            None
        DESCRIPTION
            Calculates the customer's cost
        SIDE EFFECTS
            Creates self.customer_costs
        PRECONDITIONS
            probability_default is in the (0, 1) interval
            AND loan_amount is a non-negative real number
        POSTCONDITIONS
            self.customer_costs is a list of non-negative real numbers
    END

    GETTER METHOD average_customer_cost
        INPUTS
            None
        OUTPUTS
            result: average estimated cost per customer
        DESCRIPTION
            Calculates the average cost per customer
        SIDE EFFECTS
            None
        PRECONDITIONS
            self.customer_costs exists
        POSTCONDITIONS
            result is a non-negative real number
    END

    METHOD _calculate_customer_loss
        INPUTS
            probability_default: customer's estimated PD
            AND loan_amount: customer's approved loan amount
        OUTPUTS
            None
        DESCRIPTION
            Calculates customer losses
        SIDE EFFECTS
            Creates self.customer_losses
        PRECONDITIONS
            probability_default is in the (0, 1) interval
            AND loan_amount is a non-negative real number
        POSTCONDITIONS
            self.customer_losses is a list of non-negative real numbers
    END

    GETTER METHOD average_customer_loss
        INPUTS
            None
        OUTPUTS
            result: average estimated loss per customer
        DESCRIPTION
            Calculates the average loss per customer
        PRECONDITIONS
            self.customer_losses exists
        POSTCONDITIONS
            result is a non-negative real number
    END
END

CLASS FeatureEngineeringInterface
    """
    Implements the feature engineering API. Its responsibility is to process
    data for the model.
    """

    METHOD __init__
        INPUTS
            _validated: an object of validated information to store inside the
            object
        OUTPUTS
            An object of CLASS FeatureEngineeringInterface
        DESCRIPTION
            Instantiates an object of the CLASS FeatureEngineeringInterface
        SIDE EFFECTS
            None
        PRECONDITIONS
            _validated.features must not be empty
        POSTCONDITIONS
            self.features exists and is a combination of features and
                features_to_create
            AND self.features_to_create exists and is of required type
    END

    CLASS METHOD new
        INPUTS
            features: a list of strings representing features to process
            AND features_to_create: a mapping of strings to booleans to flag
                which features must be created
        OUTPUTS
            An object of CLASS FeatureEngineeringInterface
        DESCRIPTION
            Class constructor
        PRECONDITIONS
            None
        POSTCONDITIONS
            features is not empty and is of required type
            AND features_to_create is either empty or has implemented methods
                for creation
    END

    TEMPLATE METHOD _make_feature_foo
        INPUTS
            None
        OUTPUTS
            feature: a list of values for a feature
        DESCRIPTION
            Describes a template for creating an arbitrary feature FOO. If FOO
            is not in self.features_to_create, then _make_feature_foo is
            skipped. Each feature in self.features_to_create.keys() must have
            a method implemented by this template with name _make_feature_<key>
        PRECONDITIONS
            self.features_to_create exists and is of required type
        POSTCONDITIONS
            feature exists and is of required type
    END

    GETTER METHOD pipeline
        INPUTS
            None
        OUTPUTS
            p: A Pipeline object that implements the feature engineering
                strategy
        DESCRIPTION
            Instantiates a feature engineering pipeline
        PRECONDITIONS
            self.features exists
        POSTCONDITIONS
            p exists
    END
END

CLASS ModelInterface
    """
    Implements model fitting API. Its responsibility is to fit the model and
    use it for making reliable predictions.
    """

    METHOD __init__
        INPUTS
            _validated: an object of validated information to store inside the
            object
        OUTPUTS
            An object of CLASS ModelInterface
        DESCRIPTION
            Instantiates an object of the CLASS ModelInterface
        SIDE EFFECTS
            None
        PRECONDITIONS
            _validated.features must not be empty
            AND _validated.algorithm must be one among a finite set of 
                possibilities
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

    CLASS METHOD new
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
    
    GETTER METHOD is_fitted
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
            self._raw_predictions exists
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
            self._raw_predictions conforms to the raw prediction's contract 
            established by the self.data_interface
    END

    GETTER METHOD predictions
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

### Data types

[expected credit loss]: https://primaconsulting.org/ecl-model-ifrs-9-examples/
[Assumptions]: #assumptions
[splitting strategy]: #splitting-strategy
[log-loss]: https://en.wikipedia.org/wiki/Cross-entropy
[Brier score]: https://en.wikipedia.org/wiki/Brier_score
[value-at-risk]: https://en.wikipedia.org/wiki/Value_at_risk
[RMSE]: https://en.wikipedia.org/wiki/Root_mean_square_deviation
[¹]: https://www.emergentmind.com/topics/categorical-machine-learning-methods
[Feature engineering]: #feature-engineering
[permutation importance]: https://scikit-learn.org/stable/modules/permutation_importance.html
