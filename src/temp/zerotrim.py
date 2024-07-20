import re

RE_TRZEROES = re.compile(r'(^\d+\.\d*)0+$')

def remove_trailing_zeroes(invalue: float) -> str:
    str_value = str(invalue)
    if not RE_TRZEROES.search(str_value):
        return str_value

    str_value = RE_TRZEROES.findall(str_value)[0]  # type: str
    return str_value.rstrip('.')


def main():

    array = [
        1750,
        1105.100180,
        183.2383047,
        1744.0,
        45.000000000001
    ]

    for value in array:
        print(remove_trailing_zeroes(value))




if __name__ == '__main__':
    main()