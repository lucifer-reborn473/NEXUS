import pytest
from ..src.calci import *


def test_basic_expression():
    expr = "var integer x= (2+ 1)"
    val = e(parse(expr))
    assert val == "Context(variables={'x': VariableInfo(value=3, dtype='integer', redundant=None)})"

# if __name__ == "__main__":
#     pytest.main()