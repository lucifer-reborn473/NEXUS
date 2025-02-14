import unittest
from src.parser import parse
from src.tokens import Token, KeywordToken, NumberToken, OperatorToken, VarToken, SemicolonToken
from src.evaluator import e
from src.context import Context

class TestParser(unittest.TestCase):

    def setUp(self):
        self.context = Context()

    def test_while_loop(self):
        code = """
        var integer x = 0;
        while x < 5 do
            x = x + 1;
        end
        """
        ast = parse(code)
        self.assertIsNotNone(ast)
        result = e(ast, self.context)
        self.assertEqual(self.context.get_variable('x').value, 5)

    def test_while_loop_with_display(self):
        code = """
        var integer x = 0;
        while x < 3 do
            display x;
            x = x + 1;
        end
        """
        ast = parse(code)
        self.assertIsNotNone(ast)
        with self.assertLogs() as log:
            e(ast, self.context)
        self.assertIn('0', log.output[0])
        self.assertIn('1', log.output[1])
        self.assertIn('2', log.output[2])

if __name__ == '__main__':
    unittest.main()