class Constant:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        """Get the constant`s value"""
        return self._value

    def __str__(self):
        return str(self._value)

class Variable:
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

    def evaluate(self,**kwargs):
        pass

    def variable_names(self):
        pass

    def __str__(self):
        pass

def create_constant(name):
    return Constant(name)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):
    return Operator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)
