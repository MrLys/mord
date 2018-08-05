import secrets
import string
import math
def get_ascii_characters():
    return string.ascii_letters + string.digits + string.punctuation

def get_words():
    try:
        with open('/usr/share/dict/words') as f:
            return [word.strip() for word in f]
    except FileNotFoundError efnfe:
        return []

def generate_passphrase(word_num=5):
    if word_num > 15:
        print(word_num, "words is a thad redundant.")
        word_num = 15
    words = get_words()
    if not words:
        print("Dictionary could not be found, will therefor not be generating",
                "a passphrase, but a strong random password.",
        return ''.join(secrets.choice(get_ascii_characters()) for i in
            range(word_num*8))

    return ' '.join(secrets.choice(words) for i in range(word_num))

def generate_passphrase_characters(min_characters=24):
    # Average word len in dic(on mac) is 9.6 chars.
    if min_characters < 12:
        print("Having a passphrase with less than 12 characters are not acceptable.  You'll get a larger one!")
        min_characters=24
    word_num = math.ceil(min_characters/9.6)
    words = get_words()
    if not words:
        print("Dictionary could not be found, will therefor not be generating",
                "a passphrase, but a strong random password.",
        return ''.join(secrets.choice(get_ascii_characters()) for i in
            range(word_num*8))
    pharse = ' '.join(secrets.choice(words) for i in range(word_num))
    while len(phrase) < min_characters:
        phrase += secrets.choice(words)
    return phrase


if __name__ == '__main__':
    print("This is not runnable! import it and use the functions!")
