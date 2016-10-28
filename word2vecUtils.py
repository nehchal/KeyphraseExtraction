import math


def normalize(a):
    length = 0
    for x in a:
        length += x * x
    length **= 0.5
    if length == 0:
        return a
    b = [x / length for x in a]
    return b


def cosine_sim(a, b):
    summation = 0
    for i in range(len(a)):
        summation += a[i] * b[i]
    return summation


def sigmoid(x):
    return 1 / (1 + math.exp(-6 * x))


def find_longest_matching_ngrams(words):
    ngram_long_list = []
    words_included = set()
    num_words = len(words)
    ngram_size = num_words
    while len(words_included) < num_words and ngram_size > 0:
        temp_set = set()
        for i in range(num_words - ngram_size + 1):
            if words[i] not in words_included:
                ngram = '_'.join(words[i:i + ngram_size])
                is_ngram_in_vocab = ngram in W1
                if is_ngram_in_vocab:
                    ngram_arr = ngram.split('_')
                    are_all_stopWords = True
                    for aNgram in ngram_arr:
                        temp_set.add(aNgram)
                        if aNgram not in stopwords:
                            are_all_stopWords = False
                    if not are_all_stopWords:
                        ngram_long_list.append(ngram)
        for word in temp_set:
            words_included.add(word)
        ngram_size -= 1
    return ngram_long_list


def find_ngrams(words):
    words = find_longest_matching_ngrams(words)
    temp_set = set(words)
    for word in words:
        if word not in W1 or word in stopwords or word.isdigit():
            temp_set.discard(word)
    words = list(temp_set)
    n_grams = []
    n = len(words)
    for i in range(n):
        for j in range(i):
            n_grams.append(words[j] + '-' + words[i])
    for i in range(n):
        for j in range(i):
            for k in range(j):
                n_grams.append(words[k] + '-' + words[j] + '-' + words[i])
    return n_grams


def add_vectors(a, b):
    result = []
    for i in range(len(a)):
        result.append(a[i] + b[i])
    return result


def find_similarity_between_phrases(phrase1, phrase2):
    phrase1 = phrase1.lower().rstrip()
    phrase2 = phrase2.lower().rstrip()
    phrase1_ngrams = find_longest_matching_ngrams(phrase1.split())
    phrase2_ngrams = find_longest_matching_ngrams(phrase2.split())
    return cosine_sim(find_phrase_vector(phrase1_ngrams), find_phrase_vector(phrase2_ngrams))


def find_phrase_vector(tempSet):
    context_vector = [0.0 for i in range(v_size)]
    for word in tempSet:
        context_vector = add_vectors(context_vector, W1[word])
    return normalize(context_vector)


def load_stopwords():
    with open("/home/maverick/Download/stopwords.txt") as f:
        for line in f:
            stopwords.add(line.rstrip())


def initialise():
    print "Loading word2vec vectors..."
    load_stopwords()
    f = open("vectors.txt", "r")
    vocab_size, size = map(int, f.readline().split())
    for i in range(vocab_size):
        temp = f.readline()
        word = temp.split()[0]
        word = unicode(word, "utf-8")
        temp = map(float, temp.split()[1:])
        W1[word] = normalize(temp)
    f.close()
    print "Loaded word2vec vectors. Fire in the hole."


def main():
    initialise()
    while True:
        query1 = raw_input()
        query2 = raw_input()
        print(query1, query2)
        if query1 == "EXIT":
            return
        print(find_similarity_between_phrases(query1, query2))


v_size = 200
W1 = {}
W2 = {}
stopwords = set()
if __name__ == "__main__":
    main()
