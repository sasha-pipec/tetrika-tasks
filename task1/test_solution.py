import pytest

from solution import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def returns_str(a: int, b: int) -> str:
    return a + b


def test_correct_types_for_args():
    assert sum_two(2, 3) == 5


def test_correct_types_for_kwargs():
    assert sum_two(a=2, b=3) == 5


def test_correct_types_for_mixed_params():
    assert sum_two(2, b=3) == 5


def test_wrong_types_for_args():
    with pytest.raises(TypeError):
        sum_two(2.0, 3.0)


def test_wrong_types_for_kwargs():
    with pytest.raises(TypeError):
        sum_two(a=2.0, b=3.0)


def test_wrong_types_for_mixed_params():
    with pytest.raises(TypeError):
        sum_two(2.0, b=3.0)


def test_wrong_return_type():
    with pytest.raises(TypeError):
        returns_str(1, 2)
