"""input/output functions"""
import csv
import os
import pickle
import sys
from pathlib import Path

import numpy as np



def _ensure_weights(graph):
    """ensure that graphs edges have a weights value"""
    for u, v in graph.edges:
        if "weight" not in graph[u][v]:
            graph[u][v]["weight"] = 1.0


def _set_node_features(graph):
    """If no node features, set it to 0."""
    for node in graph.nodes:
        if "feat" not in graph.nodes[node]:
            graph.nodes[node]["feat"] = [0]

        feat_shape = np.shape(graph.nodes[node]["feat"])
        if len(feat_shape) == 0:
            graph.nodes[node]["feat"] = [graph.nodes[node]["feat"]]
        elif len(feat_shape) > 1:
            raise Exception("Please provide flat node features vector.")


def save_analysis(X, explainer, shap_values, folder=".", filename="analysis_results"):
    """save results of analysis"""
    if not Path(folder).exists():
        os.mkdir(folder)

    with open(os.path.join(folder, filename + ".pkl"), "wb") as f:
        pickle.dump([X, explainer, shap_values], f)


def load_analysis(folder="/", filename="analysis_results"):
    """save results of analysis"""
    with open(os.path.join(folder, filename + ".pkl"), "rb") as f:
        return pickle.load(f)


def save_dataset(graphs, labels, filename, folder="./datasets"):
    """Save a dataset in a pickle"""
    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(os.path.join(folder, filename + ".pkl"), "wb") as f:
        #pickle.dump([graphs, labels], f)
        pickle.dump(graphs, f)


def load_dataset(filename):
    """load a dataset from a pickle"""
    with open(filename, "rb") as f:
        #graphs, labels = pickle.load(f)
        return pickle.load(f)
    #print(graphs)
    #cleaned_graphs = []
    #for i, graph in enumerate(graphs):
    #    if len(graph) > MIN_NUM_NODES:
    #        graph.label = labels[i]
    #        _set_graph_id(graph, i)
    #        _set_node_features(graph)
    #        _ensure_weights(graph)
    #        cleaned_graphs.append(graph)
    #return cleaned_graphs


def save_features(features, feature_info, graphs, filename="./features.pkl"):
    """Save the features in a pickle"""
    if not Path(filename).parent.is_dir():
        Path(filename).parent.mkdir()

    pickle.dump(
        [features, feature_info, graphs], open(filename, "wb"),
    )


def load_features(filename="features.pkl"):
    """Save the features in a pickle"""
    return pickle.load(open(filename, "rb"))
