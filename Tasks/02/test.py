import unittest
import solution


class SolutionTest(unittest.TestCase):
    def test_create_expression(self):
        plus = solution.create_operator('+', lambda lhs, rhs: lhs + rhs)
        minus = solution.create_operator('-', lambda lhs, rhs: lhs - rhs)
        times = solution.create_operator('*', lambda lhs, rhs: lhs * rhs)
        six = solution.create_constant(6)
        nine = solution.create_constant(9)
        expression = solution.create_expression((six, times, nine))
        self.assertEqual(expression.evaluate(),54)
        expression = solution.create_expression((six, plus, nine))
        self.assertEqual(expression.evaluate(),15)
        expression = solution.create_expression((nine, minus, six))
        self.assertEqual(expression.evaluate(),3)

    def test_create_constant(self):
        constant = solution.create_constant(5)
        self.assertEqual(constant.evaluate(), 5)

    def test_add(self):
        plus = solution.create_operator('+', lambda lhs, rhs: lhs + rhs)
        x = solution.create_variable('x')
        y = solution.create_variable('y')
        expression = solution.create_expression((x, plus, y))
        self.assertEqual(expression.evaluate(x=5, y=3), 8)

    def test_add_constant_and_variable(self):
        y = solution.create_variable('y')
        twelve = solution.create_constant(12)
        expression = y + twelve
        self.assertEqual(expression.evaluate(y=3), 15)
        expression = twelve + y
        self.assertEqual(expression.evaluate(y=3), 15)

    def test_sub(self):
        minus = solution.create_operator('-', lambda lhs, rhs: lhs - rhs)
        x = solution.create_variable('x')
        y = solution.create_variable('y')
        expression = solution.create_expression((x, minus, y))
        self.assertEqual(expression.evaluate(x=5, y=3), 2)

    def test_mul(self):
        times = solution.create_operator('*', lambda lhs, rhs: lhs * rhs)
        x = solution.create_variable('x')
        y = solution.create_variable('y')
        expression = solution.create_expression((x, times, y))
        self.assertEqual(expression.evaluate(x=5, y=3), 15)

if __name__ == '__main__':
    unittest.main()
