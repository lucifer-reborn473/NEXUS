import pytest

def pytest_ignore_collect(collection_path):
    return collection_path.name in ('basic_test.py', 'operation_test.py', 'project_euler_codes.py')

