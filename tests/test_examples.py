def test_while_loop_execution():
    # Example code demonstrating a while loop
    code = """
    var integer x = 0;
    while x < 5 do
        x = x + 1;
    end
    display x;
    """

    # Expected output after executing the code
    expected_output = 5

    # Execute the code and capture the output
    from context import Context
    from evaluator import e
    from parser import parse

    context = Context()
    statements = parse(code).statements

    # Redirect output to capture display statements
    import io
    import sys
    output = io.StringIO()
    sys.stdout = output

    for stmt in statements:
        e(stmt)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check if the output matches the expected output
    assert output.getvalue().strip() == str(expected_output), f"Expected {expected_output}, but got {output.getvalue().strip()}"