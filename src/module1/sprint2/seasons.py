import math
from datetime import date
from num2words import num2words

def get_word(num):
    table = {
        '0': '',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
        '10': 'ten',
        '11': 'eleven',
        '12': 'twelve',
        '13': 'thirteen',
        '14': 'fourteen',
        '15': 'fifteen',
        '16': 'sixteen',
        '17': 'seventeen',
        '18': 'eighteen',
        '19': 'nineteen',
        '20': 'twenty',
        '30': 'thirty',
        '40': 'forty',
        '50': 'fifty',
        '60': 'sixty',
        '70': 'seventy',
        '80': 'eighty',
        '90': 'ninety'
    }
    return table[str(num)]

def get_num_split(num: int) -> dict:
    num = int(num)
    if num > 99:
        raise ValueError
    holder = dict()

    def get_value(num, div = 1):
        print(f'num: {num}')
        print(f'in holder total: {sum(holder.values())}')

        return int(
            (num - sum(holder.values()))% (10 * div))

    # teens!
    holder['ones'] = num % 10
    holder['tens'] = get_value(num, 10)

    if holder['tens'] == 10 and holder['ones'] > 0:
        holder['teens'] = holder['tens'] + holder['ones']
        holder['tens'] = 0
        holder['ones'] = 0
    else:
        holder['teens'] = 0

    # holder['hundreds'] = get_value(num, 100)
    # holder['thousands'] = get_value(num, 1_000)
    # holder['tenthousands'] = get_value(num, 10_000)
    # holder['hundredthousands'] = get_value(num, 100_000)
    # holder['millions'] = get_value(num, 1_000_000)
    # holder['tenmillions'] = get_value(num, 10_000_000)
    return holder

def get_words_for_num(minutes: int) -> str:
    holder = get_num_split(minutes)

    wording = list()
    if holder['tens'] > 0:
        wording.append(get_word(holder['tens']))

    if holder['teens'] > 0:
        wording.append(get_word(holder['teens']))

    if holder['ones'] > 0:
        wording.append(get_word(holder['ones']))

    return " ".join(wording)

def using_num2words(num):
    as_words = num2words(num)
    as_words = as_words[0].upper() + as_words[1:]
    print(f'{as_words} minutes')


def main():

    # dob_yyyymmdd = input("Date of Birth: ")
    today = date.today()
    # dob = date.fromisoformat(dob_yyyymmdd)

    #minutes = int((today-dob).total_seconds()/60)

    #num_to_string(minutes)
    #print(minutes)

    print(get_words_for_num(5))
    print(get_words_for_num(17))
    print(get_words_for_num(63))


if __name__ == '__main__':
    main()
