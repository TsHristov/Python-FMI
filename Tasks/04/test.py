import unittest
import solution


class TestCritic(unittest.TestCase):
    def test_indentation(self):
        code = ('def ugly(indent):\n'
                '     return indent')
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[2]), {'indentation is 5 instead of 4'})
        code = ("def some_func():\n"
                "    for char in a_variable:\n"
                "         if char != 'a':\n"
                "              for _ in range(10):\n"
                "                print('SOOOO MUUUCH INDENTATION')\n")
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[4]), {'indentation is 5 instead of 4'})
        self.assertSetEqual(set(issues[3]), {'indentation is 5 instead of 4'})

    def test_two_statements_on_one_line(self):
        code = 'a = 5; b = 6'
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[1]),
                            {'multiple expressions on the same line'})

    def test_too_deep_nesting(self):
        code = ("def some_func():\n"
                "    for char in a_variable:\n"
                "        if char != 'a':\n"
                "            for _ in range(10):\n"
                "                print('SOOOO MUUUCH INDENTATION')\n")
        issues = solution.critic(code, max_nesting=3)
        self.assertSetEqual(set(issues[5]), {'nesting too deep (4 > 3)'})

    def test_long_line_with_several_statements(self):
        code = ("def some_func():\n"
                "    a_variable = 'some text';"
                " another_variable = 'some more text';"
                " even_moar_variables = 'just for to pass the time'")
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[2]), {
            'line too long (116 > 79)',
            'multiple expressions on the same line'
        })

    def test_max_arity(self):
        code = ("def f(a, b, c, d):\n"
                "    for i in range(a, b):\n"
                "        print(i)\n")
        issues = solution.critic(code, max_arity=3)
        self.assertSetEqual(set(issues[1]), {
            'too many arguments (4 > 3)'
        })

    def test_check_methods_per_class(self):
        code = ("class A:\n"
                "    def __init__(self):\n"
                "        pass\n"
                "    def first(self):\n"
                "        pass\n"
                "    def second(self):\n"
                "        pass\n"
                "    def third(self):\n"
                "        pass\n")
        issues = solution.critic(code, methods_per_class=3)
        self.assertSetEqual(set(issues[8]), {
            'too many methods in class (4 > 3)'
        })
        issues = solution.critic(code)
        self.assertFalse(issues)

    def test_check_trailing_whitespace(self):
        code = ("def f(): \n"
                "    for i in range(10):\n"
                "        print(i)  \n")
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[1]), {
            'trailing whitespace'
        })
        self.assertSetEqual(set(issues[3]), {
            'trailing whitespace'
        })

if __name__ == '__main__':
    unittest.main()
