import datetime
from time import time

from Lab3.api import create_account, make_bet
from Lab3.mt import MersenneRng


def get_mt_generator(account_id, first_timestamp, second_timestamp):
    response = make_bet('Mt', account_id, 1, 0)
    seed = first_timestamp

    while True:
        generator = MersenneRng(seed)
        new_generated_value = generator.get_random_number()
        seed += 1
        if new_generated_value == response['realNumber'] or seed > second_timestamp + 1:
            break

    return generator


def crack_mt():
    first_timestamp = int(time()) - 1
    account = create_account()
    second_timestamp = int(time())

    generator = get_mt_generator(account['id'], first_timestamp, second_timestamp)

    money = 0
    while money < 1_000_000:
        response = make_bet('Mt', account['id'], 10, generator.get_random_number())
        money = response['account']['money']


if __name__ == "__main__":
    crack_mt()