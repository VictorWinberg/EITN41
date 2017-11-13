
def Luhn_check_digit(account_number):
    index = account_number[::-1].find('X')
    account_number = account_number.replace('X', '0')
    numbers = list(map(int, account_number))[::-1]
    double_even = [x * 2 if i % 2 == 1 else x for (i, x) in enumerate(numbers)]
    sum_digits = [sum(map(int, str(x))) for x in double_even]

    total = sum(sum_digits)
    check_digit = total * 9 % 10

    if index % 2 == 1:
        if check_digit % 2 == 1:
            check_digit += 9
        check_digit //= 2

    return check_digit


digits = []
while True:
    try:
        digits.append(Luhn_check_digit(input('')))
    except EOFError:
        break

print('Digits:', ''.join(map(str, digits)))