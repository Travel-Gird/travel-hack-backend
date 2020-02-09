from datetime import date, datetime


def birthday_to_age(birthday) -> int:
    today = date.today()
    birthday = datetime.strptime(birthday, '%m/%d/%Y')
    return today.year - birthday.year - \
           ((today.month, today.day) < (birthday.month, birthday.day))


if __name__ == '__main__':
    print(birthday_to_age('03/18/2000'))
