# nyt-comments


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
