"""
Data Science Module 1 Sprint 2 challenge: Calculator
"""
__author__ = "@mjuuti"
__version__ = "1.0.0"

import inspect


class Calculator:
    """
    Calculator class for basic operations. All action methods return instance reference for command chaining
    """

    last_action = (None, None)
    _memory = 0  # type: float

    @property
    def value(self) -> float:
        """
        Get memory value from the calculator. If value is integer return without trailing zeroes
        :return: memory value as float
        """
        if int(self._memory) == self._memory:
            return int(self._memory)
        return self._memory

    @value.setter
    def value(self, number: float):
        """
        Set memory value to the calculator
        :param number: float value
        :return: None
        """
        self._memory = number

    def set(self, number: float):
        """
        Set memory value to a specific number like in the beginning you would type "8 + 3" rather than "+ 8 + 3"
        :param number: Value to store
        :return: Instance reference
        """
        self.value = number
        self._set_last_action(number)
        return self

    def add(self, number: float):
        """
        Add value to calculator memory value
        :param number: Number to add
        :return: Instance reference
        """
        self.value += number
        self._set_last_action(number)
        return self

    def subtract(self, number: float):
        """
        Subtract value from calculator memory
        :param number: Number to subtract
        :return: Instance reference
        """
        return self.add(-number)

    def multiply(self, number: float):
        """
        Multiply value from calculator memory
        :param number: Number to multiply with
        :return: Instance reference
        """
        self.value *= number
        self._set_last_action(number)
        return self

    def divide(self, number: float):
        """
        Divide value from calculator memory
        :param number: Number to divide with
        :return: Instance reference
        """
        return self.multiply(1.0/number)

    def power(self, number: float = 2):
        """
        Take value from calculator memory and power it to given number
        :param number: Number to power to. Defaults to square (2)
        :return: Instance reference
        """
        self.value **= number
        self._set_last_action(number)
        return self

    def root(self, number: float = 2):
        """
        Take Nth root from the value in calculator memory
        :param number: Nth root. Defaults to square (2)
        :return: Instance reference
        """
        return self.power(1.0/number)

    def clear_memory(self):
        """
        Clean calculator memory by setting it to value 0
        :return: Instance reference
        """
        self.set(0)
        return self

    def repeat(self):
        """
        Repeat last action, similar to pressing '=' button on pocket calculator
        :return:Instance referene
        """
        action, value = self.last_action  # type: str, float
        if action:
            self.__getattribute__(action)(value)
        return self

    def _set_last_action(self, number: float):
        """
        Store last action and number used for repeat purposes
        :param number: number used
        :return: None
        """
        action = inspect.stack()[1][3]
        self.last_action = (action, number)


if __name__ == '__main__':
    calc = Calculator()
    print("Example: (3v8 / 2 * 3)^3 + 1 - 18")
    print(calc.set(8).root(3).divide(2).multiply(3).power(3).add(1).subtract(18).value)


