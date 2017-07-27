class BinaryOperator:
    def __init__(self, symbol, function):
        self._symbol = symbol
        self._function = function

    def __call__(self, lhs, rhs):
        return self._function(lhs, rhs)

    def __str__(self):
        return str(self._symbol)


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
        pass

    def __truediv__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __and__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __or__(self, other):
        pass


class Constant(OperationsMixin):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        """Get the constant`s value"""
        return self._value

    def evaluate(self, **kwargs):
        return self._value

    def __str__(self):
        return str(self._value)


class Variable(OperationsMixin):
    def __init__(self, name):
        self._name = name
        self._value = None

    @property
    def name(self):
        """Get the variable name"""
        return self._name

    @property
    def value(self):
        """Get the variable value"""
        return self._value

    @value.setter
    def value(self, val):
        """Set the variable value"""
        self._value = val

    def evaluate(self, **kwargs):
        return kwargs[self._name]

    def __str__(self):
        return str(self._name)


class Expression:
    def __init__(self, expression_structure):
        self._expression_structure = expression_structure
        self._lhs, self._operator, self._rhs = self._expression_structure

    def evaluate(self, **kwargs):
        lhs = self._lhs.evaluate(**kwargs)
        rhs = self._rhs.evaluate(**kwargs)
        return self._operator(lhs, rhs)

    def variable_names(self):
        operands = [self._lhs, self._rhs]
        variables = [x for x in operands if isinstance(x, Variable)]
        names = [x.name for x in variables]
        return names

    def __str__(self):
        return (str(self._lhs), str(self._operator), str(self._rhs))


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return BinaryOperator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)
