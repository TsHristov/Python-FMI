import unittest
import solution


class SolutionTest(unittest.TestCase):
    def test_create_constant(self):
        constant = solution.create_constant(5)
        self.assertEqual(constant.evaluate(), 5)

    def test_create_expression(self):
        plus = solution.create_operator('+', lambda lhs, rhs: lhs + rhs)
        minus = solution.create_operator('-', lambda lhs, rhs: lhs - rhs)
        times = solution.create_operator('*', lambda lhs, rhs: lhs * rhs)
        x = solution.create_variable('x')
        nine = solution.create_constant(9)
        expression = solution.create_expression((x, plus, nine))
        self.assertEqual(expression.evaluate(x=6), 15)
        expression = solution.create_expression((x, minus, nine))
        self.assertEqual(expression.evaluate(x=6), -3)
        expression = solution.create_expression((x, times, nine))
        self.assertEqual(expression.evaluate(x=6), 54)

    def test_language_literals(self):
        x = solution.create_variable('x')
        expression = (x + 3).evaluate(x=1)
        self.assertEqual(expression, 4)

    def test_nested_expression(self):
        x = solution.create_variable('x')
        y = solution.create_variable('y')
        twelve = solution.create_constant(12)
        times = solution.create_operator('*', lambda lhs, rhs: lhs * rhs)
        plus =  solution.create_operator('+', lambda lhs, rhs: lhs + rhs)
        # import pdb; pdb.set_trace()
        expression = solution.create_expression((x, plus, (y, times, twelve)))
        expression = expression.evaluate(x=1, y=1)
        self.assertEqual(expression, 13)
        expression = solution.create_expression(((x, plus, y), times, twelve))
        expression = expression.evaluate(x=1, y=1)
        self.assertEqual(expression, 24)


    def test_get_variable_names(self):
        plus = solution.create_operator('+', lambda lhs, rhs: lhs + rhs)
        x = solution.create_variable('x')
        nine = solution.create_constant(10)
        expression = solution.create_expression((x,plus,nine))
        self.assertEqual(expression.variable_names(), ('x',))

    def test_add_constant_and_variable(self):
        y = solution.create_variable('y')
        twelve = solution.create_constant(12)
        expression = y + twelve
        self.assertEqual(expression.evaluate(y=3), 15)
        expression = twelve + y
        self.assertEqual(expression.evaluate(y=3), 15)

    def test_sub_constant_and_variable(self):
        y = solution.create_variable('y')
        twelve = solution.create_constant(12)
        expression = y - twelve
        self.assertEqual(expression.evaluate(y=13), 1)
        expression = twelve - y
        self.assertEqual(expression.evaluate(y=10), 2)

    def test_mul_constant_and_variable(self):
        y = solution.create_variable('y')
        ten = solution.create_constant(10)
        expression = y * ten
        self.assertEqual(expression.evaluate(y=13), 130)
        expression = ten * y
        self.assertEqual(expression.evaluate(y=13), 130)

if __name__ == '__main__':
    unittest.main()
