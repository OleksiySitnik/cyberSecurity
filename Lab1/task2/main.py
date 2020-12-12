import math
from binascii import unhexlify

cipher = b'1c41023f564b2a130824570e6b47046b521f3f5208201318245e0e6b40022643072e13183e51183f5a1f3e4702245d4b285a1b23561965133f2413192e571e28564b3f5b0e6b50042643072e4b023f4a4b24554b3f5b0238130425564b3c564b3c5a0727131e38564b245d0732131e3b430e39500a38564b27561f3f5619381f4b385c4b3f5b0e6b580e32401b2a500e6b5a186b5c05274a4b79054a6b67046b540e3f131f235a186b5c052e13192254033f130a3e470426521f22500a275f126b4a043e131c225f076b431924510a295f126b5d0e2e574b3f5c4b3e400e6b400426564b385c193f13042d130c2e5d0e3f5a086b52072c5c192247032613433c5b02285b4b3c5c1920560f6b47032e13092e401f6b5f0a38474b32560a391a476b40022646072a470e2f130a255d0e2a5f0225544b24414b2c410a2f5a0e25474b2f56182856053f1d4b185619225c1e385f1267131c395a1f2e13023f13192254033f13052444476b4a043e131c225f076b5d0e2e574b22474b3f5c4b2f56082243032e414b3f5b0e6b5d0e33474b245d0e6b52186b440e275f456b710e2a414b225d4b265a052f1f4b3f5b0e395689cbaa186b5d046b401b2a500e381d4b23471f3b4051641c0f2450186554042454072e1d08245e442f5c083e5e0e2547442f1c5a0a64123c503e027e040c413428592406521a21420e184a2a32492072000228622e7f64467d512f0e7f0d1a'


LETTERS_FREQUENCY = {
    'e': 0.1202,
    't': 0.910,
    'a': 0.812,
    'o': 0.768,
    'i': 0.731,
    'n': 0.695,
    's': 0.628,
    'r': 0.602,
    'h': 0.592,
    'd': 0.432,
    'l': 0.398,
    'u': 0.288,
    'c': 0.271,
    'm': 0.261,
    'f': 0.230,
    'y': 0.211,
    'w': 0.209,
    'g': 0.203,
    'p': 0.182,
    'b': 0.149,
    'v': 0.111,
    'k': 0.069,
    'x': 0.017,
    'q': 0.011,
    'j': 0.010,
    'z': 0.007,
}

def get_keylength(ciphertext):
    variants = [ciphertext[i:] + ciphertext[:i] for i in range(1, len(ciphertext))]
    for v in variants:
        frequency = 0
        for i in range(0, len(variants)):
            if v[i] == ciphertext[i]:
                frequency += 1
        print(frequency)
    return variants


def get_chars(cipher_bytes, n, k):
    return [cipher_bytes[i] for i in range(len(cipher_bytes)) if i % n == k]


def chi_sqr(text):
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    result = 0
    for char in ALPHABET:
        count = text.count(char)
        expected_count = math.ceil(len(text) * LETTERS_FREQUENCY[char])
        chi = ((count - expected_count) ** 2) / expected_count

        result += chi
    return result


def decrypt_repeating_xor(encrypted_text_bytes, key_bytes):
    decoded = "".join(
        map(
            chr,
            [byte ^ key_bytes[i % len(key_bytes)] for i, byte in enumerate(encrypted_text_bytes)]
        )
    )
    return decoded


def calculate_key(byte_array, key_length):
    key_bytes = []
    for i in range(key_length):
        chunk = get_chars(byte_array, key_length, i)
        variants = []

        for caesar_key in range(0, 256):
            decrypted_chunk = decrypt_repeating_xor(chunk, [caesar_key])
            chi_sqr_val = chi_sqr(decrypted_chunk)
            variants.append((decrypted_chunk, chi_sqr_val, caesar_key))

        suitable = min(variants, key=lambda v: v[1])
        key_bytes.append(suitable[2])
    print(decrypt_repeating_xor(byte_array, key_bytes))


if __name__ == "__main__":
    decoded = list(unhexlify(cipher))
    get_keylength(decoded)

    keylength = int(input('KeyLength:'))

    print(calculate_key(decoded, keylength))
