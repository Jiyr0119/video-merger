import pytest
from myproject.calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(1, 2) == 3
    assert calculator.add(-1, 1) == 0
    assert calculator.add(0.1, 0.2) == pytest.approx(0.3)

def test_subtract(calculator):
    assert calculator.subtract(3, 2) == 1
    assert calculator.subtract(1, 1) == 0
    assert calculator.subtract(0.3, 0.1) == pytest.approx(0.2)

def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6
    assert calculator.multiply(-2, 3) == -6
    assert calculator.multiply(0.1, 0.2) == pytest.approx(0.02)

def test_divide(calculator):
    assert calculator.divide(6, 2) == 3
    assert calculator.divide(5, 2) == 2.5
    assert calculator.divide(-6, 2) == -3

def test_divide_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(1, 0)