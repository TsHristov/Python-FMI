import operator


class BinaryOperator:
    def __init__(self, symbol, function):
        self._symbol = symbol
        self._function = function

    def __call__(self, lhs, rhs):
        #return Expression((lhs, self._function, rhs))
        return self._function(lhs, rhs)

    def __str__(self):
        return self._symbol


class OperatorsMixin:
    __OPERATORS = {
        'add':      BinaryOperator('+',  operator.add),
        'sub':      BinaryOperator('-',  operator.sub),
        'mul':      BinaryOperator('*',  operator.mul),
        'truediv':  BinaryOperator('/',  operator.truediv),
        'floordiv': BinaryOperator('//', operator.floordiv),
        'mod':      BinaryOperator('%',  operator.mod),
        'lshift':   BinaryOperator('<<', operator.lshift),
        'rshift':   BinaryOperator('>>', operator.rshift),
        'and':      BinaryOperator('&',  operator.and_),
        'or':       BinaryOperator('^',  operator.or_),
        'xor':      BinaryOperator('|',  operator.xor),
    }

    def __init__(self):
        """On initialization generates all operators"""
        for name, operator in self.__OPERATORS.items():
            OperatorsMixin.create_operator(name, operator)

    @classmethod
    def create_operator(cls, name, operator):
        def set_operator(self, other):
            return Expression((self, operator, other))

        def set_reverse_operator(self, other):
            return Expression((other, operator, self))
        setattr(cls, "__{}__".format(name), set_operator)
        setattr(cls, "__r{}__".format(name), set_reverse_operator)


class Constant(OperatorsMixin):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def evaluate(self, **kwargs):
        return self._value

    def __str__(self):
        return str(self._value)


class Variable(OperatorsMixin):
    def __init__(self, name):
        super().__init__()
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
        if hasattr(self._lhs, 'evaluate'):
            lhs = self._lhs.evaluate(**kwargs)
        else:
            lhs = Constant(self._lhs).evaluate(**kwargs)
        if hasattr(self._rhs, 'evaluate'):
            rhs = self._rhs.evaluate(**kwargs)
        else:
            rhs = Constant(self._rhs).evaluate(**kwargs)
        return self._operator(lhs, rhs)

    def variable_names(self):
        operands = [self._lhs, self._rhs]
        variables = [x for x in operands if isinstance(x, Variable)]
        names = tuple(x.name for x in variables)
        return names

    def __str__(self):
        result = "({} {} {})".format(self._lhs, self._operator, self._rhs)
        return result


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return BinaryOperator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)
