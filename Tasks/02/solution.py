class BinaryOperator:
    def __init__(self, symbol, function):
        self._symbol = symbol
        self._function = function

    def __call__(self, lhs, rhs):
        return self._function(lhs, rhs)

    def __str__(self):
        return self._symbol


class OperationsMixin:
    __operators = {
        '+':  BinaryOperator('+',  lambda x, y: x + y),
        '-':  BinaryOperator('-',  lambda x, y: x - y),
        '*':  BinaryOperator('*',  lambda x, y: x * y),
        '/':  BinaryOperator('/',  lambda x, y: x / y),
        '//': BinaryOperator('//', lambda x, y: x // y),
        '%':  BinaryOperator('%',  lambda x, y: x % y),
        '<<': BinaryOperator('<<', lambda x, y: x << y),
        '>>': BinaryOperator('>>', lambda x, y: x >> y),
        '&':  BinaryOperator('&',  lambda x, y: x & y),
        '^':  BinaryOperator('^',  lambda x, y: x ^ y),
        '|':  BinaryOperator('|',  lambda x, y: x | y),
    }

    def __add__(self, other):
        expression = self, self.__operators['+'], other
        return Expression(expression)

    def __sub__(self, other):
        expression = self, self.__operators['-'], other
        return Expression(expression)

    def __mul__(self, other):
        expression = self, self.__operators['*'], other
        return Expression(expression)

    def __truediv__(self, other):
        expression = self, self.__operators['/'], other
        return Expression(expression)

    def __floordiv__(self, other):
        expression = self, self.__operators['//'], other
        return Expression(expression)

    def __mod__(self, other):
        expression = self, self.__operators['%'], other
        return Expression(expression)

    def __lshift__(self, other):
        expression = self, self.__operators['<<'], other
        return Expression(expression)

    def __rshift__(self, other):
        expression = self, self.__operators['>>'], other
        return Expression(expression)

    def __and__(self, other):
        expression = self, self.__operators['&'], other
        return Expression(expression)

    def __xor__(self, other):
        expression = self, self.__operators['^'], other
        return Expression(expression)

    def __or__(self, other):
        expression = self, self.__operators['|'], other
        return Expression(expression)


class Constant(OperationsMixin):
    def __init__(self, value):
        self._value = value

    def evaluate(self, **kwargs):
        return self._value

    def __str__(self):
        return str(self._value)


class Variable(OperationsMixin):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def evaluate(self, **kwargs):
        return kwargs[self._name]

    def __str__(self):
        return str(self._name)


class Expression:
    def __init__(self, expression_structure):
        self._lhs, self._operator, self._rhs = expression_structure

    def evaluate(self, **kwargs):
        lhs = self._lhs.evaluate(**kwargs)
        rhs = self._rhs.evaluate(**kwargs)
        return self._operator(lhs, rhs)

    def variable_names(self):
        operands = [self._lhs, self._rhs]
        variables = [x for x in operands if isinstance(x, Variable)]
        names = tuple(x.name for x in variables)
        return names

    def __str__(self):
        result = "{}{}{}".format(self._lhs, self._operator, self._rhs)
        return result


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return BinaryOperator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)
