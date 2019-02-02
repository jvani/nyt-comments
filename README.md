# nyt-comments
This project creates a graph of New York Times Articles (node), Users (node), and user's comments (relationships). The data was taken from kaggle: see [New York Times Comments](https://www.kaggle.com/aashita/nyt-comments/home).

> The data contains information about the comments made on the articles published in New York Times in Jan-May 2017 and Jan-April 2018. The month-wise data is given in two csv files - one each for the articles on which comments were made and for the comments themselves. The csv files for comments contain over 2 million comments in total with 34 features and those for articles contain 16 features about more than 9,000 articles.

Running this project will start 2 services:
<table border="0">
  <tr>
    <th>Neo4J Graph @ <a href=http://localhost:7474>http://localhost:7474<a></th>
    <th>Toy Recommender @ <a href=http://localhost:5000>http://localhost:5000<a></th>
  </tr>
  <tr>
    <td><img alt="Neo4J Graph" src="https://github.com/jvani/nyt-comments/blob/master/docs/graphex.png"></img></td>
    <td><img alt="Toy Recommender" src="https://github.com/jvani/nyt-comments/blob/master/docs/recex.png"></img></td>
  </tr>
</table>

## Requirements
```
git
docker
docker-compose
```
**Note:** Downloading our dataset (via `setup.sh`) uses kaggle API credentials stored in `~/.kaggle/kaggle.json`. See [API Credentials](https://github.com/Kaggle/kaggle-api#api-credentials) from the `kaggle-api` docs.

## Setup
```
git clone https://github.com/jvani/nyt-comments.git && \
  cd nyt-comments && \
  ./setup.sh
```
The `setup.sh` script will do the following:
1. Pull used docker images.
2. Download neo4j plugins (written to `$PWD/plugins`)
3. Download our dataset (written to `$PWD/kaggle/`)
4. Create our graph data (written to `$PWD/import`)
5. Import our data into neo4j (database files will be written to `$PWD/data`) 
6. Start our docker-compose services: neo4j and toy recommender. **NOTE:** a jupyter server is included but the image is HUGE and off by default; uncomment in the `docker-compose.yaml` if desired.
7. Run graph statistics on our database.
