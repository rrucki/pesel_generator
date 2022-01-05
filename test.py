from faker import Faker
import datetime
import functools
import pandas as pd
import random
import timeit
fake = Faker(['pl_PL'])


def generate_ssns(record_count):
    records = pd.DataFrame([[fake.ssn()] for _ in range(record_count)],
                           columns=["PESEL"])
    return records


def generate_unique_ssns(record_count, start_date, end_date, person_sex):
    record_list = []
    for _ in range(record_count):
        random_date = start_date + datetime.timedelta(days=random.randrange(
            (end_date - start_date).days))
        record_list.append(fake.pesel(date_of_birth=random_date,
                                      sex=person_sex))
    records = pd.DataFrame(record_list, columns=["PESEL"])
    return records


def validate_ssn(pesel, sex, birth_date):
    template_pesel = fake.pesel(date_of_birth=birth_date)
    checksum = (int(pesel[0])*1 + int(pesel[1])*3 + int(pesel[2])*7
                + int(pesel[3])*9 + int(pesel[4])*1 + int(pesel[5])*3
                + int(pesel[6])*7 + int(pesel[7])*9 + int(pesel[8])*1
                + int(pesel[9])*3 + int(pesel[10])*1)

    if template_pesel[:6] == pesel[:6] and str(checksum)[-1] == '0':
        if int(pesel[9]) % 2 == 0 and sex == 'F':
            return print("PESEL: {} is valid".format(pesel))
        elif int(pesel[9]) % 2 != 0 and sex == 'M':
            return print("PESEL: {} is valid".format(pesel))
        elif sex != 'F' and sex != 'M':
            return print("PESEL: {} is valid".format(pesel))
        else:
            return print("PESEL: {} is invalid".format(pesel))
    else:
        return print("PESEL: {} is invalid".format(pesel))


def main():
    generate_ssns(5)  # boot loop to reduce initial lag
    print("generate_ssns - 10 records in \t\t\t{} second"
          .format(timeit.Timer(functools.partial(generate_ssns, 10))
                  .timeit(1)))
    print("generate_ssns - 100 records in \t\t\t{} second"
          .format(timeit.Timer(functools.partial(generate_ssns, 100))
                  .timeit(1)))
    print("generate_ssns - 1000 records in \t\t{} second"
          .format(timeit.Timer(functools.partial(generate_ssns, 1000))
                  .timeit(1)))
    print("generate_unique_ssns - 1000 records in \t\t{} second"
          .format(timeit.Timer(functools.partial(generate_unique_ssns, 1000,
                                                 datetime.date(1920, 1, 20),
                                                 datetime.date(1994, 10, 10),
                                                 'M')).timeit(1)))
    validate_ssn('71102690031', 'M', datetime.date(1971, 10, 26))
    return


if __name__ == '__main__':
    main()
