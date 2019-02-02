# -*- coding: utf-8 -*-
import py2neo
import pandas as pd
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

graph = py2neo.Graph('http://neo4j:7474')


def yield_record(cursor):
    halt = False
    while not halt:
        try:
            yield cursor.next().data()
        except:
            halt = True

def random_article(graph):
    """"""
    op = "MATCH (n:ARTICLE) WITH n, rand() as r ORDER BY r RETURN n LIMIT 1"   
    failure = 0
    article = None
    while (article is None) and (failure < 5):
        try:
            cur = graph.run(op)
            article = cur.next().data()['n']
            if article['headline'] == 'Unknown':
                article = None
        except:
            failure +=1
    if failure >= 5:
        raise ValueError('Neo4J query failure.')
    return article

def connected_articles(graph, articleID):
    """"""
    op = """MATCH (n:ARTICLE {{articleID: '{0}'}})-[]-(:USER)-[]-(m:ARTICLE)
    WHERE NOT m.articleID = '{0}'
    RETURN m""".format(articleID)
    cur = graph.run(op)
    df = pd.DataFrame([rr['m'] for rr in yield_record(cur)])
    comments = pd.DataFrame(df.groupby('articleID').size().rename('Comments'))
    recs = df.merge(comments, left_on='articleID', right_on='articleID') \
            .drop_duplicates() \
            .sort_values(['Comments', 'pagerank'], ascending=False)
    return recs[recs.headline != 'Unknown']

@app.route('/')
def home():
    rarticle = random_article(graph)
    recs = connected_articles(graph, rarticle['articleID'])
    return render_template('home.html', rarticle=rarticle, recommendations=recs.head().to_dict(orient='rows'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

