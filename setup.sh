#!/bin/bash
# -- Pull docker images.
docker pull neo4j
docker pull python
# -- If the import files don't exist, run download.sh script.
if [[ -e $PWD/import/users.csv && -e $PWD/import/articles.csv && -e $PWD/import/comments.csv ]]; then
    echo "Import files already exist.";
else
    echo 'Downloading project files...';
    docker run --rm -v $PWD:/root/ -v $HOME/.kaggle:/root/.kaggle python /root/scripts/download.sh;
fi
# -- If the neo4j database doesn't exist, import data to the database.
if [[ -e $PWD/data/databases/graph.db ]]; then
    echo "neo4j database files already exist."
else
    echo 'Importing data to neo4j...';
    docker run --rm -v $PWD/data/:/data -v $PWD/import:/var/lib/neo4j/import neo4j \
        /var/lib/neo4j/bin/neo4j-admin import \
        --nodes /var/lib/neo4j/import/articles.csv \
        --nodes /var/lib/neo4j/import/users.csv \
        --relationships /var/lib/neo4j/import/comments.csv;
fi
# -- Start neo4j and toy recommender.
echo 'Starting docker-compose services...'
docker-compose up -d;
# -- Wait until the neo4j server is up...
until (($(curl -s -o /dev/null -w "%{http_code}" http://localhost:7474) == 200)); do
    echo "neo4j is unavailable, sleeping..."
    sleep 10
done
# -- ...and calculate graph_stats.
docker run --rm --network nyt-comments_default -v $PWD:/root/ python /root/scripts/graph_stats.sh
