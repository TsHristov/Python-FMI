import re
import ast
from collections import defaultdict


class CodeErrors:
    def line_too_long(self, actual, allowed):
        return 'line too long ({} > {})'.format(
            actual, allowed
        )

    def multiple_expressions(self):
        return 'multiple expressions on the same line'

    def nesting_too_deep(self, actual, allowed):
        return 'nesting too deep ({} > {})'.format(
            actual, allowed
        )

    def indentation(self, actual, allowed):
        return 'indentation is {} instead of {}'.format(
            actual, allowed
        )

    def too_many_methods_per_class(self, actual, allowed):
        return 'too many methods in class ({} > {})'.format(
            actual, allowed
        )

    def too_many_arguments(self, actual, allowed):
        return 'too many arguments ({} > {})'.format(
            actual, allowed
        )

    def trailing_whitespace(self):
        return 'trailing whitespace'

    def too_many_lines(self, actual, allowed):
        return 'method with too many lines ({} > {})'.format(
            actual, allowed
        )


class CodeCritic:
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
        methods = {method for method in
                   dir(type(self)) if
                   callable(getattr(type(self), method)) and not
                   method.startswith('__')}
        # Filter out only the 'check_' methods:
        return filter(lambda method:
                      method.startswith('check'),
                      methods)

    def analyze(self, **kwargs):
        """
           Inpect the code and call all instance
           check methods on it.
        """
        methods = self.__get_instance_methods()
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
        code = enumerate(self.code.splitlines(), start=1)
        for line_number, line in code:
            line_length = len(line)
            if line_length > default_length:
                self.issues[line_number].add(
                    self.code_errors.line_too_long(line_length, default_length)
                    )

    def check_has_semicolons(self, **kwargs):
        """Inspect the code for semicolon separated statements."""
        code = enumerate(self.code.splitlines(), start=1)
        for line_number, line in code:
            if re.search(';', line):
                self.issues[line_number].add(
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
        nodes = [(node, node.lineno) for node
                 in ast.walk(self.parsed_code.body[0])
                 if hasattr(node, 'body')]
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
            # Use the default value instead:
            indentation_size = self.DEFAULT_RULES['indentation_size']
        # Traverse the nodes and find those that are nested
        # (have 'body' attribute).
        nodes = [node for node in ast.walk(self.parsed_code.body[0])
                 if hasattr(node, 'body')]
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
        """
           Inspect the code for trailing whitespace
           at the end of the line.
        """
        try:
            forbid_trailing_whitespace = kwargs['forbid_trailing_whitespace']
        except KeyError:
            forbid_trailing_whitespace = self.DEFAULT_RULES['forbid_trailing_whitespace']
        if not forbid_trailing_whitespace:
            return
        code = enumerate(self.code.splitlines(), start=1)
        for line_number, line in code:
            # Check whether there are trailing
            # whitespaces at the end of the line:
            if re.search('\s$', line):
                self.issues[line_number].add(
                    self.code_errors.trailing_whitespace()
                )

    def check_lines_per_function(self, **kwargs):
        """
           Inspect the code for too many lines
           per function/method.
        """
        try:
            max_lines = kwargs['max_lines_per_function']
        except KeyError:
            return
        function_definition = self.parsed_code.body[0]
        if not isinstance(function_definition, ast.FunctionDef):
            return
        code_lines = self.code.splitlines()[1:]
        # Filter out the lines, which do
        # not consist only of whitespaces:
        logic_lines = len(list(filter(lambda line:
                          line != re.search('\s+', line).group(),
                          code_lines)))
        if logic_lines > max_lines:
            line_number = function_definition.lineno
            self.issues[line_number].add(
                self.code_errors.too_many_lines(
                    logic_lines, max_lines)
                )


def critic(code, **rules):
    return CodeCritic(code).analyze(**rules)
