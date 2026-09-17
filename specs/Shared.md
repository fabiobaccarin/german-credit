# Common patterns for services

This file describes common patterns to be used for all services, thus providing
a single source of truth for common behavior.

## Initialization

All services follow the *smart constructor pattern*. Specifically, all services
expose a `new` `classmethod` that takes user-friendly data types as inputs,
validates them against [domain models] and calls the service's `__init__`
method.

The `__init__` method is implemented exclusively as a private method that
simply allocates validated inputs to object attributes. Here is a simplified
example of this pattern for the [data service class]:

```python
class DataService:
    """Implements data reading, writing and validation (simplified example)"""

    def __init__(self, _validated: ValidatedInputs) -> None:
        self.dataset = _validated.dataset
        self.model_schema = _validated.model_schema
    
    @classmethod
    def new(
        cls,
        url: URL | None = None,
        checksum: MD5ChecksumString | None = None,
        file_path: FilePath,
        model_schema_value: ModelSchemaValue
    ) -> 'Foo':
        # Validates the dataset against its Pydantic domain model
        dataset = Dataset(url=url, checksum=checksum, file_path=file_path)
        
        # Validates the model schema
        model_schema = ModelSchema(value=model_schema_value)
        
        # Build the validated inputs container
        _validated = ValidatedInputs(dataset=dataset, model_schema=model_schema)

        return cls(_validated)
```

## See also

[Domain]

[domain models]: Domain.md
[data service class]: Data.md
[Domain]: Domain.md