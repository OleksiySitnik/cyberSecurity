from Lab3.api import make_bet, create_account
from Lab3.mt import MersenneRng
from z3 import *


def untemper(out):
    y1 = BitVec('y1', 32)
    y2 = BitVec('y2', 32)
    y3 = BitVec('y3', 32)
    y4 = BitVec('y4', 32)
    y = BitVecVal(out, 32)
    s = Solver()
    equations = [
        y2 == y1 ^ (LShR(y1, 11)),
        y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
        y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
        y == y4 ^ (LShR(y4, 18))
    ]
    s.add(equations)
    s.check()
    return s.model()[y1].as_long()


def recover_state_mt(numbers):
    state = []
    for n in numbers[0:624]:
        state.append(untemper(n))
    return state


def crack_better_mt(account_id):
    state = []
    for i in range(624):
        print(i)
        response = make_bet('BetterMt', account_id, 1, 0)
        state.append(response['realNumber'])

    recovered_state = recover_state_mt(state)
    generator = MersenneRng()
    generator.state = recovered_state

    money = 0
    while money < 1_000_000:
        response = make_bet('BetterMt', account_id, 1, generator.get_random_number())
        money = response['account']['money']
        print(money)


if __name__ == "__main__":
    account = create_account()
    crack_better_mt(account['id'])
