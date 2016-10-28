from __future__ import division
import math
import pprint
import networkx
import itertools
import word2vecUtils
import codecs

from SpacyUtil import SpacyNlpUtil

__author__ = 'shashank'


def read_weights(vectors_file):
    f = open(vectors_file, "r+")
    word_vec = {}
    n, s = map(int, f.readline().split())
    for i in range(n):
        line = f.readline()
        w = line.split()[0]
        line = line.split()[1:]
    word_vec[w] = map(float, line)
    f.close()
    return word_vec


def remove_candidates_not_in_vocab(candidates):
    filtered_candidates = []
    for cand in candidates:
        cand = cand.lower().rstrip()
        ngrams = word2vecUtils.find_longest_matching_ngrams(cand.split())
        if len(ngrams) != 0:
            filtered_candidates.append(cand)
    return filtered_candidates


def add_outgoing_weights(element, node_to_weight_sum_map, toAdd):
    if element in node_to_weight_sum_map:
        node_to_weight_sum_map[element] = node_to_weight_sum_map[element] + toAdd
    else:
        node_to_weight_sum_map[element] = toAdd


def score_by_word2vec(possible_candidates):
    filtered_candidates = remove_candidates_not_in_vocab(possible_candidates)
    graph = networkx.DiGraph()
    graph.add_nodes_from(set(filtered_candidates))
    prob_sum = {}
    pair_prob = {}
    for candidatePair in itertools.combinations(filtered_candidates, 2):
        first_candidate = candidatePair[0]
        second_candidate = candidatePair[1]
        scores_cand_ = word2vecUtils.find_similarity_between_phrases(first_candidate, second_candidate)
        scores_cand_ = word2vecUtils.sigmoid(scores_cand_)
        add_outgoing_weights(first_candidate, prob_sum, scores_cand_)
        add_outgoing_weights(second_candidate, prob_sum, scores_cand_)
        pair_prob[(first_candidate, second_candidate)] = scores_cand_
        pair_prob[(second_candidate, first_candidate)] = scores_cand_

    for candidatePair in itertools.combinations(filtered_candidates, 2):
        first_candidate = candidatePair[0]
        second_candidate = candidatePair[1]
        if prob_sum[first_candidate] != 0:
            graph.add_weighted_edges_from([(first_candidate, second_candidate, pair_prob[(first_candidate, second_candidate)] / prob_sum[first_candidate])])
        if prob_sum[second_candidate] != 0:
            graph.add_weighted_edges_from([(second_candidate, first_candidate, pair_prob[(second_candidate, first_candidate)] / prob_sum[second_candidate])])

    ranks = networkx.pagerank(graph, max_iter=1000)
    pprint.pprint(sorted(ranks.iteritems(), key=lambda x: x[1], reverse=True))


text_title = "Semantic Keyphrase Extraction"
text = codecs.open("/home/shashank/Downloads/topic-file.txt", "r", "utf-8").read()

word2vecUtils.initialise()
spacyObj = SpacyNlpUtil()
candidates = spacyObj.tagger(text)['noun_chunks']
score_by_word2vec(candidates)