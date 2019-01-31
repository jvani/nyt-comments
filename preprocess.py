# -*- coding: utf-8 -*-
import os
import logging
import pandas as pd
from collections import defaultdict


logging.basicConfig(level='INFO', format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Preprocessor:
    def __init__(self, data_directory):
        dfs = self.load_all(data_directory)
        self.articles = pd.concat(dfs['Articles']).drop_duplicates('articleID:ID')
        self.users = pd.concat(dfs['Users']).drop_duplicates('userID:ID')
        self.comments = pd.concat(dfs['Comments']).drop_duplicates()
        self.comments = self.comments[
            (self.comments['articleID:END_ID'].isin(self.articles['articleID:ID'])) &
            (self.comments['userID:START_ID'].isin(self.users['userID:ID']))
        ]
            
    @classmethod
    def load_all(cls, data_directory):
        """"""
        dfs = defaultdict(list)
        # -- List all in the given data.
        for fname in os.listdir(data_directory):
            fpath = os.path.join(data_directory, fname)
            # -- For all article files...
            if 'Articles' in fname:
                dfs['Articles'].append(cls.load_from_articles(fpath))
            # -- For all comment files...
            elif 'Comments' in fname:
                users, comments = cls.load_from_comments(fpath)
                dfs['Comments'].append(comments)
                dfs['Users'].append(users)
        return dfs

    @staticmethod
    def load_from_articles(fpath):
        """"""
        logging.info('Creating graph: {}'.format(fpath))
        # -- Load article data and create article nodes.
        columns = ['articleID', 'headline', 'byline', 'newDesk', 'pubDate', 'webURL']
        articles = pd.read_csv(fpath, dtype=str, usecols=columns).fillna('')
        articles.rename(columns={'articleID': 'articleID:ID'}, inplace=True)
        articles[':LABEL'] = 'ARTICLE'
        return articles

    @staticmethod
    def load_from_comments(fpath):
        """"""
        logging.info('Creating graph: {}'.format(fpath))
        # -- Load comment data.
        columns = ['userID', 'userDisplayName', 'userLocation', 'articleID']
        df = pd.read_csv(fpath, dtype=str, usecols=columns)
        # -- Create user nodes.
        users = df[columns[:-1]].drop_duplicates('userID').rename(columns={'userID': 'userID:ID'})
        users[':LABEL'] = 'USER'
        # -- Create comment relationships.
        comments = df[['userID', 'articleID']].drop_duplicates().rename(columns={'userID': 'userID:START_ID', 'articleID': 'articleID:END_ID'})
        comments[':TYPE'] = 'COMMENTED'
        return (users, comments)

    def write(self, outdir='import'):
        """"""
        if not os.path.isdir(outdir): os.mkdir(outdir)
        for attr in ['articles', 'users', 'comments']:
            fpath = os.path.join(outdir, '{}.csv'.format(attr))
            getattr(self, attr).to_csv(fpath, index=False)

if __name__ == "__main__":
    HOME = os.path.expanduser('~')
    OUTDIR = os.path.join(HOME, 'import')

    if len(os.listdir(OUTDIR)) != 3:
        pp = Preprocessor(os.path.join(HOME, 'kaggle'))
        pp.write(OUTDIR)
