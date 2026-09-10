CLASS ModelValidator
    """
    Provides data validation methods for ensuring correct model execution
    """
    
    METHOD __init__
        INPUTS
            input_schema: an object containing field restrictions for inputs
            AND output_schema: an object containing field restrictions for
                outputs
        OUTPUTS
            None
        DESCRIPTION
            Initializes an object of CLASS ModelValidator
        SIDE EFFECTS
            None
        PRECONDITIONS
            input_schema must not be empty and must be of required type
            AND output_schema must not be empty and must be of required type
        POSTCONDITIONS
            self.input_schema exists
            AND self.output_schema exists
        INVARIANTS
            input_schema doesn't no change during method execution
            AND output_schema doesn't no change during method execution
    END

    METHOD validate_input
        INPUTS
            data: Data in tabular form
        OUTPUTS
            None
        DESCRIPTION
            Check input data conforms to the data contract implemented by the
            Data IO module
        SIDE EFFECTS
            None
        PRECONDITIONS
            data is not empty and is of correct type
        POSTCONDITIONS
            data conforms to the contract specified by self.input_schema
    END

    METHOD validate_output
        INPUTS
            data: Data in tabular form
        OUTPUTS
            None
        DESCRIPTION
            Check output data conforms to the data contract implemented by
            the DATA IO module
        SIDE EFFECTS
            None
        PRECONDITIONS
            data is not empty and is of correct type
        POSTCONDITIONS
            data conforms to the contract specified by self.output_schema
    END
END

FUNCTION new_model_validator
    INPUTS
        input_schema: an object containing field restrictions for inputs
        AND output_schema: an object containing field restrictions for outputs
    OUTPUTS
        An object of CLASS ModelValidator
    PRECONDITIONS
        None
    POSTCONDITIONS
        input_schema is not empty and is of required type
        AND output_schema is not empty and is of required type
END

METHOD validate_predictions
        INPUTS
            predictions: A list of predictions made by an object of CLASS 
                ModelInterface
        OUTPUTS
            predictions
        DESCRIPTION
            Checks that outputted predictions are in the correct format
        SIDE EFFECTS
            None
        PRECONDITIONS
            None
        POSTCONDITIONS
            preditions is not an empty list
            AND All predictions are allowed string values
        INVARIANTS
            predictions must not change during the method's execution
    END