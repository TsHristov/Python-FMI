import re
import ast
from collections import defaultdict


class CodeErrors:
    def line_too_long(self, actual, allowed):
        if actual > allowed:
            return 'line too long ({} > {})'.format(actual, allowed)

    def multiple_expressions(self):
        return 'multiple expressions on the same line'

    def nesting_too_deep(self, actual, allowed):
        if actual > allowed:
            return 'nesting too deep ({} > {})'.format(actual, allowed)

    def indentation(self, actual, allowed):
        if actual > allowed:
            return 'indentation is {} instead of {}'.format(actual, allowed)

    def too_many_methods_per_class(self, actual, allowed):
        if actual > allowed:
            return 'too many methods in class ({} > {})'.format(actual, allowed)

    def too_many_arguments(self, actual, allowed):
        if actual > allowed:
            return 'too many arguments ({} > {})'.format(actual, allowed)

    def trailing_whitespace(self):
        pass

    def too_many_lines(self, actual, allowed):
        pass


class CodeAnalyzer:
    # Set of rules with default values
    # that apply to the code under inspection.
    DEFAULT_RULES = {
        'line_length': 79,
        'forbid_semicolons': True,
        'max_nesting': None,
        'indentation_size': 4,
        'methods_per_class': None,
        'max_arity': None,
        'forbid_trailing_whitespace': True,
        'max_lines_per_function': None
    }

    def __init__(self, code):
        self.parsed_code = ast.parse(code)
        self.code = code
        # Keys are the line numbers
        # at which errors were found.
        self.issues = defaultdict(set)
        self.code_errors = CodeErrors()

    def __get_instance_methods(self):
        """Return set of all instance methods."""
        return {method for method in
                dir(type(self)) if
                callable(getattr(type(self), method)) and not
                method.startswith('__')}

    def analyze(self, **kwargs):
        """
           Inpect the code and call all instance
           check methods on it.
        """
        methods = self.__get_instance_methods()
        methods = list(filter(lambda method:
                              method.startswith('check'),
                              methods))
        for method in methods:
            # Call each method:
            getattr(type(self), method)(self, **kwargs)
        return self.issues

    def check_line_length(self, **kwargs):
        """Inspect the code for too long lines."""
        try:
            default_length = kwargs['line_length']
        except KeyError:
            # Use the default value instead:
            default_length = self.DEFAULT_RULES['line_length']
        for line_number, line in enumerate(self.code.splitlines()):
            line_length = len(line)
            if line_length > default_length:
                self.issues[line_number+1].add(
                    self.code_errors.line_too_long(line_length, default_length)
                    )

    def check_has_semicolons(self, **kwargs):
        """Inspect the code for semicolon separated statements."""
        for line_number, line in enumerate(self.code.splitlines()):
            if re.search('(;)', line):
                self.issues[line_number+1].add(
                    self.code_errors.multiple_expressions()
                )

    def check_nesting(self, **kwargs):
        """Inspect the code for too much nested expressions."""
        try:
            max_nesting = kwargs['max_nesting']
        except KeyError:
            return
        # Traverse the nodes and find those that are nested
        # (have 'body' attribute).
        nodes = [(node, node.lineno) for node in ast.walk(self.parsed_code.body[0])
                 if 'body' in node._fields]
        nesting_level = len(nodes)
        if nesting_level > max_nesting:
            # The line number where the error was found
            # is the next one (thus + 1):
            line_number = nodes[-1][1] + 1
            self.issues[line_number].add(
                self.code_errors.nesting_too_deep(
                    nesting_level, max_nesting
                )
            )

    def check_indentation(self, **kwargs):
        """Inspect the code for indentation size errors."""
        try:
            indentation_size = kwargs['indentation_size']
        except KeyError:
            indentation_size = self.DEFAULT_RULES['indentation_size']
        # Traverse the nodes and find those that are nested
        # (have 'body' attribute).
        nodes = [node for node in ast.walk(self.parsed_code.body[0])
                 if 'body' in node._fields]
        # Use the previous line offset
        # as a guide for the next line indentation.
        last_offset = 0
        for node in nodes:
            line_number = node.body[0].lineno
            col_offset = node.body[0].col_offset
            if col_offset > last_offset + indentation_size:
                offset = col_offset - last_offset
                self.issues[line_number].add(
                    self.code_errors.indentation(offset, indentation_size)
                )
            last_offset = col_offset

    def check_methods_per_class(self, **kwargs):
        """
           Inspect the code for too many methods per
           class.
        """
        try:
            methods_per_class = kwargs['methods_per_class']
        except KeyError:
            return
        klass = self.parsed_code.body[0]
        if not isinstance(klass, ast.ClassDef):
            return
        methods = [(node, node.lineno) for node in ast.walk(klass)
                   if isinstance(node, ast.FunctionDef)]
        try:
            # Get the last method of the class
            # and its line number:
            line_number = methods[-1][1]
            self.issues[line_number].add(
                self.code_errors.too_many_methods_per_class(
                    len(methods), methods_per_class
                    )
                )
        except IndexError:
            return

    def check_arity(self, **kwargs):
        """
           Inspect the code for too many arguments per
           function/method.
        """
        try:
            max_arity = kwargs['max_arity']
        except KeyError:
            return
        node = self.parsed_code.body[0]
        if not isinstance(node, ast.FunctionDef):
            return
        arity = len(node.args.args)
        if arity > max_arity:
            line_number = node.lineno
            self.issues[line_number].add(
                self.code_errors.too_many_arguments(arity, max_arity)
            )

    def check_trailing_whitespace(self, **kwargs):
        pass

    def check_lines_per_function(self, **kwargs):
        pass


def critic(code, **rules):
    return CodeAnalyzer(code).analyze(**rules)
