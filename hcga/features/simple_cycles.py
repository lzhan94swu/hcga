"""Simple cycles class."""
import networkx as nx

from ..feature_class import FeatureClass, InterpretabilityScore

featureclass_name = "SimpleCycles"


class SimpleCycles(FeatureClass):
    """Simple cycles class.

    Computes features based on simple cycles (elementary circuits) of a directed graph.

    A `simple cycle`, or `elementary circuit`, is a closed path where
    no node appears twice. Two elementary circuits are distinct if they
    are not cyclic permutations of each other.

    Cycles calculations using networkx:
        `Cycles <https://networkx.org/documentation/stable/_modules/networkx/algorithms/cycles.html>`_


    References
    ----------
    .. [1] Finding all the elementary circuits of a directed graph.
       D. B. Johnson, SIAM Journal on Computing 4, no. 1, 77-84, 1975.
       https://doi.org/10.1137/0204007
    .. [2] Enumerating the cycles of a digraph: a new preprocessing strategy.
       G. Loizou and P. Thanish, Information Sciences, v. 27, 163-182, 1982.
    .. [3] A search strategy for the elementary cycles of a directed graph.
       J.L. Szwarcfiter and P.E. Lauer, BIT NUMERICAL MATHEMATICS,
       v. 16, no. 2, 192-204, 1976.

    """

    modes = ["fast", "medium", "slow"]
    shortname = "SC"
    name = "simple_cycles"
    encoding = "networkx"

    def compute_features(self):
        def simple_cycles_func(graph):
            return list(nx.simple_cycles(graph))

        self.add_feature(
            "number_simple_cycles",
            lambda graph: len(simple_cycles_func(graph)),
            "A simple closed path with no repeated nodes (except the first)",
            InterpretabilityScore(3),
        )

        self.add_feature(
            "simple_cycles_sizes",
            lambda graph: [len(i) for i in simple_cycles_func(graph)],
            "the distribution of simple cycle lengths",
            InterpretabilityScore(3),
            statistics="centrality",
        )
