#!/bin/bash
mkdir -p -m 777 $HOME/plugins && \
	mkdir -p -m 777 $HOME/import && \
	mkdir -p -m 777 $HOME/kaggle && \
	pip install kaggle pandas && \
	wget -nc -P $HOME/plugins/ https://github.com/neo4j-contrib/neo4j-graph-algorithms/releases/download/3.5.1.0/graph-algorithms-algo-3.5.1.0.jar && \
	wget -nc -P $HOME/plugins/ https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.1/apoc-3.5.0.1-all.jar && \
    kaggle datasets download aashita/nyt-comments -p $HOME/kaggle/ && \
    unzip -n $HOME/kaggle/*.zip -d $HOME/kaggle/ && \
    python $HOME/preprocess.py
