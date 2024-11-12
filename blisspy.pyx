# distutils: language = c++
# distutils: extra_compile_args = -std=c++11
# distutils: libraries = bliss

r"""
This code is based on the following:


Interface with bliss: graph (iso/auto)morphism

Implemented functions:

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`canonical_form_from_edge_list` | Return the canonical form from a given graph (could be multigraph)

AUTHORS:

    - Jernej Azarija
"""

# ****************************************************************************
#       Copyright (C) 2015 Jernej Azarija
#       Copyright (C) 2015 Nathann Cohen <nathann.cohen@gail.com>
#       Copyright (C) 2018 Christian Stump <christian.stump@gmail.com>
#       Copyright (C) 2024 Levente Bodnar <bodnalev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from libc.limits cimport LONG_MAX

cdef extern from "bliss/graph.hh" namespace "bliss":

    cdef cppclass Stats:
        Stats()

    cdef cppclass AbstractGraph:
        pass

    cdef cppclass Graph(AbstractGraph):
        Graph(unsigned int n)
        void add_edge(unsigned int v1, unsigned int v2)
        void change_color(unsigned int v, unsigned int color)
        const unsigned int* canonical_form(Stats& stats)

cdef int encoding_numbits(int n) except -1:
    """
    Return the number of bits needed to encode the numbers from 1 to n.
    In other words, the position of the highest bit set in n.
    """
    if n <= 0:
        return 0
    cdef int i = 0
    while n:
        n >>= 1
        i += 1
    return i

cdef Graph* bliss_graph_from_labelled_edges(int Vnr, int Lnr, Vout, Vin, labels, partition):
    """
    Construct a Bliss Graph from edge lists and labels.
    """
    cdef Graph* g
    cdef int i, j, x, y, lab, Pnr, Enr, logLnr = 1

    if Lnr <= 1:
        g = new Graph(Vnr)
    else:
        logLnr = encoding_numbits(Lnr)
        g = new Graph(Vnr * logLnr)
    if not g:
        raise MemoryError("Allocation failed for Graph.")

    Enr = len(Vout)

    if Lnr <= 1:
        for i in range(Enr):
            g.add_edge(Vout[i], Vin[i])
    else:
        # Arrows going up in layers
        for i in range(Vnr * (logLnr - 1)):
            g.add_edge(i, i + Vnr)

        # Edges representing the original graph with labels
        for i in range(Enr):
            x = Vout[i]
            y = Vin[i]
            lab = labels[i] + 1
            j = 0
            while lab:
                if lab & 1:
                    g.add_edge(j * Vnr + x, j * Vnr + y)
                j += 1
                lab >>= 1

    # Apply vertex partition coloring
    if partition:
        Pnr = len(partition)
        for i in range(Pnr):
            for v in partition[i]:
                for j in range(logLnr):
                    g.change_color(j * Vnr + v, j * Pnr + i)
    else:
        for j in range(logLnr):
            for v in range(Vnr):
                g.change_color(j * Vnr + v, j)

    return g

cpdef canonical_form_from_edge_list(int Vnr, list Vout, list Vin, int Lnr, list labels, list partition, bint certificate):
    """
    Return an unsorted list of labelled edges of a canonical form.

    Parameters:
        Vnr (int): Number of vertices (vertices are 0 to Vnr - 1).
        Vout (list): List of source vertices for edges.
        Vin (list): List of target vertices for edges.
        Lnr (int, optional): Number of labels. Defaults to 1.
        labels (list, optional): List of edge labels. Defaults to None.
        partition (list, optional): Partition of the vertex set. Defaults to None.
        certificate (bool, optional): Whether to return the relabeling certificate. Defaults to False.

    Returns:
        list or tuple: Canonical edge list, and optionally the relabeling certificate.
    """
    if labels is None:
        labels = []
    if partition is None:
        partition = []
    if Lnr is None:
        Lnr = 1
    if certificate is None:
        certificate = False
    # Ensure Vnr does not exceed system limits
    assert <unsigned long>(Vnr) <= <unsigned long>LONG_MAX

    cdef const unsigned int* aut
    cdef Graph* g = NULL
    cdef Stats s
    cdef dict relabel = {}
    cdef list new_edges = []
    cdef long e, f
    cdef int i, x, y, lab

    g = bliss_graph_from_labelled_edges(Vnr, Lnr, Vout, Vin, labels, partition)
    aut = g.canonical_form(s)

    for i in range(len(Vout)):
        x = Vout[i]
        y = Vin[i]
        e = aut[x]
        f = aut[y]
        if Lnr == 1:
            lab = 0 if not labels else labels[0]
        else:
            lab = labels[i]
        new_edges.append((e, f, lab) if e > f else (f, e, lab))

    if certificate:
        relabel = {v: aut[v] for v in range(Vnr)}

    if g is not NULL:
        del g

    if certificate:
        return new_edges, relabel
    return new_edges
