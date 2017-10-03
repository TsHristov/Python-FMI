import ast


class CodeErrors:
    def line_too_long(self, actual, allowed):
        pass

    def multiple_expressions_on_the_same_line(self):
        pass

    def nesting_too_deep(self, actual, allowed):
        pass

    def indentation(self, actual, size):
        if actual > size:
            return 'indentation is {} instead of {}'.format(actual, size)

    def too_many_methods_in_class(self, actual, allowed):
        pass

    def too_many_arguments(self, actual, allowed):
        pass

    def trailing_whitespace(self):
        pass

    def too_many_lines(self, actual, allowed):
        pass


class CodeAnalyzer:
    # Set of rules with default values
    # that apply to the code under inspection.
    RULES = {
        'line_length': 79,
        'forbid_semicolons': True,
        'max_nesting': None,
        'indentation_size': 4,
        'methods_per_class': None,
        'max_arity': None,
        'forbid_trailing_whitespace': True,
        'max_lines_per_function': None
    }

    def __init__(self, code, rules=None):
        self.code = ast.parse(code)
        self.rules = rules
        # Keys are the line numbers
        # at which errors were found.
        self.issues = {}
        self.code_errors = CodeErrors()

    @classmethod
    def get_instance_methods(cls):
        """Return set of all instance methods."""
        return {method for method in
                dir(cls) if
                callable(getattr(cls, method)) and not
                method.startswith('__')}

    def analyze(self):
        """Inpect the code and call all instance
           methods on it.
        """
        if not self.rules:
            methods = self.get_instance_methods()
            methods.discard('analyze')
            methods.discard('get_instance_methods')
            for method in methods:
                # Call each method:
                getattr(type(self), method)(self)
        return self.issues

    def line_length(self):
        pass

    def forbid_semicolons(self):
        pass

    def max_nesting(self):
        pass

    def indentation_size(self):
        """Inspect the code for indentation size errors."""
        #TODO: Make use of ast.NodeVisitor
        lineno = self.code.body[0].body[0].lineno
        col_offset = self.code.body[0].body[0].col_offset
        indent = self.RULES['indentation_size']
        self.issues[lineno] = {self.code_errors.indentation(col_offset, indent)}

    def methods_per_class(self):
        pass

    def max_arity(self):
        pass

    def forbid_trailing_whitespace(self):
        pass

    def max_lines_per_function(self):
        pass


def critic(code, **rules):
    return CodeAnalyzer(code).analyze()
