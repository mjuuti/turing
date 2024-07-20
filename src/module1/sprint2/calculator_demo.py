import re
RE_TRAILING_ZEROES = re.compile(r'(^\d+\.\d*)0+$')

RE_INPUT_VALIDATION = re.compile(r'^(?:[+\-*%v]?\d+|=)*$')
RE_INPUT_TOKEN = re.compile(r'([+\-*%v]?)(\d+)')

RE_QUIT = re.compile(r'quit|exit|done', re.I)

ACTION_SUBTRACT = '-'
ACTION_DIVIDE = '%'
ACTION_MULTIPLY = '*'
ACTION_ADD = '+'
ACTION_ROOT = 'v'
ACTION_EQUALS = '='
ACTION_MEMCLEAR = 'mc'


class DemoInterface:
    def display(self):
        """
        Display memory status on screen with display format handling
        :return:
        """
        print(self.remove_trailing_zeroes(self.memory))

    @staticmethod
    def remove_trailing_zeroes(input_value: float) -> str:
        """
        Convert input float to a string with trailing post-decimal point zeroes removed
        :param input_value:
        :return:
        """
        str_value = str(input_value)
        if not RE_TRAILING_ZEROES.search(str_value):
            return str_value

        str_value = RE_TRAILING_ZEROES.findall(str_value)[0]  # type: str
        return str_value.rstrip('.')


    def display_help(self):
        pass

    @staticmethod
    def validate_input(user_input):
        if RE_QUIT.search(user_input):
            sys.exit(0)
        if not RE_INPUT_VALIDATION.search(user_input):
            raise ValueError("invalid input")

    def tokenize_input(self, user_input: str):
        user_input = user_input.replace(' ', '')
        self.validate_input(user_input)
        tokens = RE_INPUT_TOKEN.findall(user_input)
        if len(tokens) > 1 and any(not action for action, value in tokens[1:]):
            raise ValueError("missing action from trailing tokens")

        return tokens


if __name__ == '__main__':
    from calculator import Calculator
    c = Calculator()
    print("# 1 -->")
    print(c.set(8).root(3).value)
    print("# 2 -->")
    print(c.set(4).add(2).subtract(1).multiply(2).value)
    print("# 3 -->")
    print(c.repeat().value)
    print("# 4 -->")
    print(c.set(5).repeat().value)
