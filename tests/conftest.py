import pytest
# def pytest_ignore_collect(path):
#     return str(path).endswith(('basic_test.py', 'operation_test.py', 'project_euler_codes.py'))
def pytest_ignore_collect(collection_path):
    return collection_path.name in ('basic_test.py', 'operation_test.py', 'project_euler_codes.py','euler_test.py')
    # return collection_path.name in ('basic_test.py', 'operation_test.py', 'project_euler_codes.py')