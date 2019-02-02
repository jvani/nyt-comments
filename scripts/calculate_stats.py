# -*- coding: utf-8 -*-
import py2neo

if __name__ == '__main__':
    graph = py2neo.Graph('http://neo4j:7474')
    # -- Calculate page rank.
    print('Calculating PageRank; see neo4j logs for progress...')
    op = ('CALL algo.pageRank(null, null, {iterations:20, dampingFactor:0.85, write: true, writeProperty:"pagerank"}) '
    'YIELD nodes, iterations, loadMillis, computeMillis, writeMillis, dampingFactor, write, writeProperty')
    graph.run(op)
    print('Completed calculating PageRank.')
    # -- Calculate connected components.
    print('Calculating connected components; see neo4j logs for progress...')
    op = ('CALL algo.unionFind(null, null, {write:true, partitionProperty:"connComponent"}) '
    'YIELD nodes, setCount, loadMillis, computeMillis, writeMillis;')
    graph.run(op)
    print('Completed calculating connected components.')

