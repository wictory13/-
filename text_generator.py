import argparse
from nltk import ngrams, RegexpTokenizer
import random


def create_parser():
    parser = argparse.ArgumentParser(description='Генератор текстов')
    parser.add_argument('text', type=str, help='текст, на основе которого будет происходить генерация')
    parser.add_argument('-n', '--count', type=int, help='количество слов в n-грамме', default=10)
    parser.add_argument('-l', '--length', type=int, help='длина текста', default=40)
    parser.add_argument('-e', '--encoding', type=str,
                        help='кодирока', default='windows-1251')
    return parser


def read_text(file, encoding):
    try:
        with open(file, encoding=encoding) as f:
            text = f.read().lower()
            tokenizer = RegexpTokenizer(r'\w+')
            return tokenizer.tokenize(text)
    except FileNotFoundError:
        print('Такого файла не существует')
        exit(1)


def generate_ngrams(text, count):
    ngram_dict = {}
    ngram_list = ngrams(text, count)
    for ngram in ngram_list:
        ngram_dict[ngram[0: count - 1]] = ngram[count - 1]
    return ngram_dict


def generate_text(ngram_dict, length):
    start = random.choice(list(ngram_dict.keys()))
    text = list(start)
    text.append(ngram_dict[start])
    for _ in range(length):
        new_words = list(start[1:])
        new_words.append(ngram_dict[tuple(start)])
        if tuple(new_words) in ngram_dict:
            text.append(ngram_dict[tuple(new_words)])
            start = new_words
        else:
            break
    print(' '.join(text))


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    text = read_text(namespace.text, namespace.encoding)
    ngram_dict = generate_ngrams(text, namespace.count)
    generate_text(ngram_dict, namespace.length - namespace.count)
