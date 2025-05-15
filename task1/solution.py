import inspect


def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        signature = inspect.signature(func)
        mapped_args = signature.bind(*args, **kwargs)

        for key, value in mapped_args.arguments.items():
            validate_type(
                value=value, expected_type=annotations.get(key)
            )

        result = func(*args, **kwargs)
        validate_type(
            value=result, expected_type=annotations.get("return")
        )

        return result

    def validate_type(value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Invalid type. Expected type: {expected_type}, got: {type(value)}"
            )

    return wrapper
