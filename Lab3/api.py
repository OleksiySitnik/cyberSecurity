import random
import uuid

import requests

BASE_URL = 'http://95.217.177.249/casino'


def create_account():
    player_id = uuid.uuid4()
    response = requests.get(f'{BASE_URL}/createacc?id=${player_id}')
    return response.json()


def make_bet(mode, player_id, amount_of_money, number_of_bet):
    response = requests.get(f'{BASE_URL}/play{mode}?id={player_id}&bet={amount_of_money}&number={number_of_bet}')
    return response.json()

