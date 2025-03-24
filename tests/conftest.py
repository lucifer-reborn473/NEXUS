import pytest

def pytest_ignore_collect(path):
    return str(path).endswith(('basic_test.py', 'operation_test.py', 'project_euler_codes.py'))

