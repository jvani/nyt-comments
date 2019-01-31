#!/bin/bash
docker run --rm -v $PWD:/root/ -v $HOME/.kaggle:/root/.kaggle python /root/download.sh && \
    docker run --rm -v $PWD/data/:/data -v $PWD/import:/var/lib/neo4j/import neo4j \
    /var/lib/neo4j/bin/neo4j-admin import \
    --nodes /var/lib/neo4j/import/articles.csv \
    --nodes /var/lib/neo4j/import/users.csv \
    --relationships /var/lib/neo4j/import/comments.csv