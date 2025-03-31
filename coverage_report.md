# Test Session Report

## Test Session Starts

- **Platform**: win32
- **Python Version**: 3.13.1
- **pytest Version**: 8.3.4
- **pluggy Version**: 1.5.0
- **Root Directory**: `C:\Users\Balgopal\compilers\Our_Compiler`
- **Config File**: `pyproject.toml`
- **Test Paths**: `tests`
- **Plugins**: `cov-6.0.0`

### Collected Tests

- **Total Tests**: 40

### Test Results

| Test File                         | Status            | Progress |
| --------------------------------- | ----------------- | -------- |
| `tests\arithmetic_test.py`      | .........         | [ 22% ]  |
| `tests\data_structs_test.py`    | ....              | [ 32% ]  |
| `tests\logical_bitwise_test.py` | ................. | [ 75% ]  |
| `tests\loop_condition_test.py`  | ..........        | [100% ]  |

---

## Warnings Summary

- **File**: `tests\conftest.py:3`
  ```plaintext
  c:\Users\Balgopal\compilers\Our_Compiler\tests\conftest.py:3: PytestRemovedIn9Warning: The (path: py.path.local) argument is deprecated, please use (collection_path: pathlib.Path)
  see https://docs.pytest.org/en/latest/deprecations.html#py-path-local-arguments-for-hooks-replaced-with-pathlib-path
    def pytest_ignore_collect(path):
  ```
- **Docs**: [Pytest Warnings Documentation](https://docs.pytest.org/en/stable/how-to/capture-warnings.html)

---

## Coverage Report

### Platform: win32

### Python Version: 3.13.1-final-0

| Name                              | Stmts | Miss | Cover | Missing Lines                                                                                                                                                                                                                            |
| --------------------------------- | ----- | ---- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src\evaluator.py`              | 232   | 57   | 75%   | 17, 24, 31, 33, 49, 51, 61, 67, 69, 75, 94, 163, 172, 196, 216, 219-221, 224-229, 232-235, 252, 255, 272-391                                                                                                                             |
| `src\lexer.py`                  | 185   | 26   | 86%   | 117, 119, 123, 125, 140, 157-160, 164-169, 175-176, 199-205, 241-243                                                                                                                                                                     |
| `src\parser.py`                 | 692   | 96   | 86%   | 222, 224, 236, 239-243, 284-285, 307-308, 337-338, 342-343, 348, 351-352, 454-455, 515-516, 535-536, 555-556, 561-568, 611-622, 635-636, 661, 671-672, 675-676, 686, 692, 726, 751-752, 818-819, 823-854, 866-867, 869-870, 872-873, 880 |
| `src\scope.py`                  | 43    | 8    | 81%   | 28, 38-41, 49, 52-54                                                                                                                                                                                                                     |
| `src\tokens.py`                 | 10    | 0    | 100%  |                                                                                                                                                                                                                                          |
| `tests\__init__.py`             | 0     | 0    | 100%  |                                                                                                                                                                                                                                          |
| `tests\arithmetic_test.py`      | 10    | 0    | 100%  |                                                                                                                                                                                                                                          |
| `tests\conftest.py`             | 3     | 0    | 100%  |                                                                                                                                                                                                                                          |
| `tests\data_structs_test.py`    | 16    | 0    | 100%  |                                                                                                                                                                                                                                          |
| `tests\logical_bitwise_test.py` | 20    | 4    | 80%   | 41-44                                                                                                                                                                                                                                    |
| `tests\loop_condition_test.py`  | 47    | 6    | 87%   | 99-140                                                                                                                                                                                                                                   |

**Total**:

- **Statements**: 1258
- **Missed**: 197
- **Coverage**: 84%

---

## Test Summary

- **Passed**: 40
- **Warnings**: 1
- **Time**: 0.54s
