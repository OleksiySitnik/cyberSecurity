import json
import math
import random
from string import ascii_uppercase as alphabet

TEXT = 'KZBWPFHRAFHMFSNYSMNOZYBYLLLYJFBGZYYYZYEKCJVSACAEFLMAJZQAZYHIJFUNHLCGCINWFIHHHTLNVZLSHSVOZDPYSMNYJXHMNODNHPATXFWGHZPGHCVRWYSNFUSPPETRJSIIZSAAOYLNEENGHYAMAZBYSMNSJRNGZGSEZLNGHTSTJMNSJRESFRPGQPSYFGSWZMBGQFBCCEZTTPOYNIVUJRVSZSCYSEYJWYHUJRVSZSCRNECPFHHZJBUHDHSNNZQKADMGFBPGBZUNVFIGNWLGCWSATVSSWWPGZHNETEBEJFBCZDPYJWOSFDVWOTANCZIHCYIMJSIGFQLYNZZSETSYSEUMHRLAAGSEFUSKBZUEJQVTDZVCFHLAAJSFJSCNFSJKCFBCFSPITQHZJLBMHECNHFHGNZIEWBLGNFMHNMHMFSVPVHSGGMBGCWSEZSZGSEPFQEIMQEZZJIOGPIOMNSSOFWSKCRLAAGSKNEAHBBSKKEVTZSSOHEUTTQYMCPHZJFHGPZQOZHLCFSVYNFYYSEZGNTVRAJVTEMPADZDSVHVYJWHGQFWKTSNYHTSZFYHMAEJMNLNGFQNFZWSKCCJHPEHZZSZGDZDSVHVYJWHGQFWKTSNYHTSZFYHMAEDNJZQAZSCHPYSKXLHMQZNKOIOKHYMKKEIKCGSGYBPHPECKCJJKNISTJJZMHTVRHQSGQMBWHTSPTHSNFQZKPRLYSZDYPEMGZILSDIOGGMNYZVSNHTAYGFBZZYJKQELSJXHGCJLSDTLNEHLYZHVRCJHZTYWAFGSHBZDTNRSESZVNJIVWFIVYSEJHFSLSHTLNQEIKQEASQJVYSEVYSEUYSMBWNSVYXEIKWYSYSEYKPESKNCGRHGSEZLNGHTSIZHSZZHCUJWARNEHZZIWHZDZMADNGPNSYFZUWZSLXJFBCGEANWHSYSEGGNIVPFLUGCEUWTENKCJNVTDPNXEIKWYSYSFHESFPAJSWGTYVSJIOKHRSKPEZMADLSDIVKKWSFHZBGEEATJLBOTDPMCPHHVZNYVZBGZSCHCEZZTWOOJMBYJSCYFRLSZSCYSEVYSEUNHZVHRFBCCZZYSEUGZDCGZDGMHDYNAFNZHTUGJJOEZBLYZDHYSHSGJMWZHWAFTIAAY'
BIGRAMS = json.load(open('english_bigrams.json'))
TRIGRAMS = json.load(open('english_trigrams.json'))


def shuffle_string(string):
    string_list = list(string)
    random.shuffle(string_list)

    return ''.join(string_list)


def swap_letters(text, index1, index2):
    text_list = list(text)
    text_list[index1], text_list[index2] = text_list[index2], text_list[index1]
    return ''.join(text_list)


def get_indexes_for_mutation(variant):
    return random.sample(range(len(variant) - 1), 4)


def mutation(variant):
    indexes = get_indexes_for_mutation(variant)
    return swap_letters(variant, indexes[0], indexes[1])


def decode(text, key):
    text_list = list(text)
    list_key = list(key)
    return ''.join(map(lambda letter: alphabet[list_key.index(letter)], text_list))


def perform_crossover(variant1, variant2):
    points = random.sample(range(len(variant1) - 1), 5)
    variant2_list = list(variant2)
    result = [None] * len(variant1)
    for index in points:
        letter = variant1[index]
        result[index] = letter

        variant2_list = list(filter(lambda char: char != letter, variant2_list))

    j = 0
    for i in range(len(result)):
        if not result[i]:
            result[i] = variant2_list[j]
            j += 1

    return ''.join(result)




def get_ngrams_statistics(text):
    bigrams = {}
    total_bigrams = 0
    trigrams = {}
    total_trigrams = 0
    for i in range(0, len(text)):
        if i < len(text) - 1:
            bigram = text[i: i + 2]

            bigrams[bigram] = bigrams[bigram] + 1\
                if bigram in bigrams else 1
            total_bigrams += 1

        if i < len(text) - 2:
            trigram = text[i: i + 3]
            trigrams[trigram] = trigrams[trigram] + 1 \
                if trigram in trigrams else 1
            total_trigrams += 1

    return bigrams, total_bigrams, trigrams, total_trigrams


def ngram_frequencies(ngrams, text_length):
    return [{'key': ngram, 'frequency': ngrams[ngram] / text_length} for ngram in ngrams]


def calculate_score(text):
    bigrams, total_bigrams, trigrams, total_trigrams = get_ngrams_statistics(text)

    bigram_frequencies = ngram_frequencies(bigrams, total_bigrams)
    trigram_frequencies = ngram_frequencies(trigrams, total_trigrams)

    bigram_score = sum(map(lambda x: abs(x['frequency'] - BIGRAMS.get(x['key'], 0)), bigram_frequencies))
    trigram_score = sum(map(lambda x: abs(x['frequency'] - TRIGRAMS.get(x['key'], 0)), trigram_frequencies))

    return 0.2 * bigram_score + 0.8 * trigram_score


def generate_initial_population(size):
    return [{'key': shuffle_string(alphabet), 'score': 0} for i in range(0, size)]


def set_fitnesses(population, text):
    for variant in population:
        if not variant['score']:
            decoded_text = decode(text, variant['key'])
            variant['score'] = calculate_score(decoded_text)


def selection(population):
    return list(sorted(population, key=lambda x: x['score']))[:math.floor(len(population) / 4)]


def crossover(population):
    if random.random() > 1 - 0.6:
        first_parent_index = random.randint(0, len(population) - 1)
        second_parent_index = random.randint(0, len(population) - 1)
        child = perform_crossover(
            population[first_parent_index]['key'],
            population[second_parent_index]['key']
        )
        if random.random() < 0.3:
            child = mutation(child)
        population.append({'key': child, 'score': 0})


def get_key(text):
    curr_population = generate_initial_population(300)
    for i in range(500):
        print(i)
        set_fitnesses(curr_population, text)
        curr_population = selection(curr_population)
        while len(curr_population) < 300:
            crossover(curr_population)

    return min(curr_population, key=lambda x: x['score'])['key']


if __name__ == "__main__":
    key = get_key(TEXT)
    print(key)
    print(decode(TEXT, key))
