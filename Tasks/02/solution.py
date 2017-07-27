class OperationsMixin:
    def __add__(self, other):
        operator = Operator('+', lambda x, y: x + y)
        expression = self, operator, other
        return Expression(expression)

class Constant(OperationsMixin):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        """Get the constant`s value"""
        return self._value

    def evaluate(self):
        return self._value

    def __str__(self):
        return str(self._value)

class Variable(OperationsMixin):
    def __init__(self, name):
        self._name  = name
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

class Operator:
    def __init__(self, symbol, function):
        self._symbol = symbol
        self._function = function

    def __call__(self, lhs, rhs):
        return self._function(lhs, rhs)

    def __str__(self):
        return str(self._symbol)

class Expression:
    def __init__(self, expression_structure):
        self._expression_structure = expression_structure
        self._lhs, self._operator, self._rhs = self._expression_structure

    def evaluate(self,**kwargs):
        if hasattr(self._lhs, 'name'):
            lhs = kwargs[self._lhs.name]
        else:
            lhs = self._lhs.value
        if hasattr(self._rhs, 'name'):
            rhs = kwargs[self._rhs.name]
        else:
            rhs = self._rhs.value
        return self._operator(lhs, rhs)

    def variable_names(self):
        operands = [self._lhs, self._rhs]
        variables = [x for x in operands if isinstance(x,Variable)]
        names = [x.name for x in variables]
        return names


    def __str__(self):
        return (str(self._lhs),str(self._operator),str(self._rhs))

def create_constant(name):
    return Constant(name)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return Operator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)
