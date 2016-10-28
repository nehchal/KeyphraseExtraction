from __future__ import division

import codecs
import itertools
import math
import pprint
import re

import networkx

from SpacyUtil import SpacyNlpUtil

__author__ = 'shashank'


def initialise_scores(candidates, text):
    global initialScores, positionArrays, tfs
    initialScores = {}
    positionArrays = {}
    tfs = {}
    new_candidates = []

    for candidate in candidates:
        loc = text.lower().find(candidate)
        if loc == -1:
            pass
        else:
            loc += 1
            pos_arr_candidate = [m.start() for m in re.finditer(candidate, text.lower())]
            if len(pos_arr_candidate) != 0:
                new_candidates.append(candidate)
                positionArrays[candidate] = pos_arr_candidate
                tfs[candidate] = len(pos_arr_candidate)
                initialScores[candidate] = math.log(1000 / loc) * len(candidate)
    return new_candidates


def modify_scores(candidates):
    new_candidates = []
    for pair in itertools.product(candidates, candidates):
        candidate = pair[0]
        bigger_candidate = pair[1]
        if len(candidate) < len(bigger_candidate):
            loc = bigger_candidate.find(candidate)
            if loc != -1:
                tfs[candidate] -= tfs[bigger_candidate]
    for candidate, score in initialScores.items():
        if score <= 0:
            pass
        else:
            initialScores[candidate] *= tfs[candidate]
            new_candidates.append(candidate)
    return new_candidates


def score_by_pagerank(candidates):
    graph = networkx.DiGraph()
    graph.add_nodes_from(set(candidates))
    for candidatePair in itertools.combinations(candidates, 2):
        first_candidate = candidatePair[0]
        second_candidate = candidatePair[1]
        edge_weight = 0
        for pos1, pos2 in itertools.product(positionArrays[first_candidate], positionArrays[second_candidate]):
            if pos1 == pos2:
                pass
            else:
                diff_pos = math.fabs(pos1 - pos2)
                edge_weight += math.log(1000 / diff_pos)
        edge_weight /= len(positionArrays[first_candidate]) * len(positionArrays[second_candidate])
        scores_cand_ = edge_weight * initialScores[first_candidate] * initialScores[second_candidate]
        graph.add_weighted_edges_from([(first_candidate, second_candidate, scores_cand_)])
        graph.add_weighted_edges_from([(second_candidate, first_candidate, scores_cand_)])
    ranks = networkx.pagerank(graph, max_iter=100)
    pprint.pprint(sorted(ranks.iteritems(), key=lambda x: x[1], reverse=True))


text = codecs.open("/home/maverick/Downloads/topic-file.txt", "r", "utf-8").read()
text_title = "Syntactic Keyphrase Extraction"

spacyObj = SpacyNlpUtil()
candidates = spacyObj.tagger(text)['noun_chunks']
candidates = initialise_scores(candidates, text)
candidates = modify_scores(candidates)
score_by_pagerank(candidates)