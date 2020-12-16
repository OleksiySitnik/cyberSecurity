from Lab3.api import make_bet, create_account

M = 2 ** 32

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)


def modinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def crack_unknown_increment(states, modulus, multiplier):
    incr = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, incr


def crack_unknown_multiplier(states, modulus=M):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)


def get_keys(player_id):

    multiplier = incr = None
    while multiplier is None or incr is None:
        first_state = make_bet('Lcg', player_id, 10, 10)['realNumber']
        second_state = make_bet('Lcg', player_id, 10, 10)['realNumber']
        states = [first_state, second_state]
        if modinv(states[1] - states[0], M):
            third_state = make_bet('Lcg', player_id, 10, 10)['realNumber']
            states.append(third_state)

            return crack_unknown_multiplier(states), states[-1]


def calculate_next_value(a, number, c):
    result = (a * number + c) % M
    if abs(result) <= 2 ** 31:
        return result
    return result - M if result > 0 else result + M


def mod(a, b):
    return ((a % b) + b) % b


if __name__ == "__main__":
    account = create_account()
    ((m, mult, increment), last_value) = get_keys(account['id'])
    next_value = calculate_next_value(mult, last_value, increment)
    bet = make_bet('Lcg', account['id'], 1, str(next_value))
    print(bet)

    money = 0
    while money < 1_000_000:
        next_value = calculate_next_value(mult, next_value, increment)
        bet = make_bet('Lcg', account['id'], 10, str(next_value))
        money = bet['account']['money']
        print(bet['account']['money'])
