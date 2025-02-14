from lexer import lex
from tokens import KeywordToken, NumberToken, VarToken, OperatorToken, SemicolonToken
import unittest

class TestLexer(unittest.TestCase):

    def test_while_keyword(self):
        input_code = "while x < 10;"
        tokens = list(lex(input_code))
        expected_tokens = [
            KeywordToken("while"),
            VarToken("x"),
            OperatorToken("<"),
            NumberToken("10"),
            SemicolonToken()
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_while_with_expression(self):
        input_code = "while (x + 1) >= 5;"
        tokens = list(lex(input_code))
        expected_tokens = [
            KeywordToken("while"),
            OperatorToken("("),
            VarToken("x"),
            OperatorToken("+"),
            NumberToken("1"),
            OperatorToken(")"),
            OperatorToken(">="),
            NumberToken("5"),
            SemicolonToken()
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_while_with_nested_statements(self):
        input_code = """
        while x < 10 {
            display x;
            x = x + 1;
        }
        """
        tokens = list(lex(input_code))
        expected_tokens = [
            KeywordToken("while"),
            VarToken("x"),
            OperatorToken("<"),
            NumberToken("10"),
            OperatorToken("{"),
            KeywordToken("display"),
            VarToken("x"),
            SemicolonToken(),
            VarToken("x"),
            OperatorToken("="),
            VarToken("x"),
            OperatorToken("+"),
            NumberToken("1"),
            SemicolonToken(),
            OperatorToken("}"),
        ]
        self.assertEqual(tokens, expected_tokens)

if __name__ == "__main__":
    unittest.main()