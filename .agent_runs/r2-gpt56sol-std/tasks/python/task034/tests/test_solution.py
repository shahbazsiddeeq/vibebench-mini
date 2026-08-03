import pytest
from src.solution import min_coins


def test_basic():
    assert min_coins([1, 5, 6, 9], 11) == 2


def test_impossible():
    assert min_coins([2], 3) == -1


def test_amount_zero():
    assert min_coins([1, 5], 0) == 0


def test_single_denomination():
    assert min_coins([5], 25) == 5


def test_classic_case():
    assert min_coins([1, 2, 5], 11) == 3


def test_negative_coin_raises():
    with pytest.raises(ValueError):
        min_coins([-1, 5], 10)


def test_zero_coin_raises():
    with pytest.raises(ValueError):
        min_coins([0, 5], 10)


def test_negative_amount_raises():
    with pytest.raises(ValueError):
        min_coins([1, 5], -1)


def test_empty_coins_nonzero_amount():
    assert min_coins([], 5) == -1


def test_empty_coins_zero_amount():
    assert min_coins([], 0) == 0


def test_unlimited_supply_reuses_denomination():
    # Only way to make 6 from a single denomination of 2 is 2+2+2.
    assert min_coins([2], 6) == 3


@pytest.mark.parametrize(
    "coins,amount,expected",
    [
        ([1], 5, 5),
        ([2, 3, 7], 7, 1),
        ([3], 7, -1),
    ],
)
def test_parametrized(coins, amount, expected):
    assert min_coins(coins, amount) == expected
