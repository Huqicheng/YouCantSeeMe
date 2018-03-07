import numpy as np
from similarity import cooccuranceSimilarityMatrix
from utils import *

class Recommender(object):
    def __init__(self):
        self.params={}

    def recommend(self,user,topN=5):
        pass

    def fit(self,data_map,options={}):
        pass

    def save(self,dir):
        pass

    def load(self,dir):
        pass


class ItemCFRecommender(Recommender):
    def __init__(self):
        super(ItemCFRecommender, self).__init__()
    
    def recommend(self,user,topN=5):
        pass
    
    def fit(self,data_map,options={}):
        similarityMatrix,user_item_matrix = cooccuranceSimilarityMatrix(data_map)
        self.params['similarity_matrix'] = similarityMatrix
        self.params['user_item_matrix'] = user_item_matrix
        self.params['item_index'] = data_map['item_index_map']
        self.params['user_index'] = data_map['user_index_map']

    def save(self,dir='./models'):
        np.save(dir+'/similarity.npy',self.params['similarity_matrix'])
        np.save(dir+'/user_item.npy',self.params['user_item_matrix'])
        save_obj(dir+'/item_index.obj',self.params['item_index'])
        save_obj(dir+'/user_index.obj',self.params['user_index'])
    
    
    def load(self,dir='./models'):
        self.params['similarity_matrix'] = np.load(dir+'/similarity.npy')[()]
        self.params['user_item_matrix'] = np.load(dir+'/user_item.npy')[()]
        self.params['item_index'] = load_obj(dir+'/item_index.obj')
        self.params['user_index'] = load_obj(dir+'/user_index.obj')


