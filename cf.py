import numpy as np
from similarity import cooccuranceSimilarityMatrix


class Recommender(object):
    def __init__(self):
        self.params={}

    def recommend(self,user,topN=5):
        pass

    def fit(self,data_map,options={}):
        pass


class ItemCFRecommender(Recommender):
    def __init__(self):
        super(ItemCFRecommender, self).__init__()
    
    def recommend(self,user,topN=5):
        pass
    
    def fit(self,data_map,options={}):
        similarityMatrix = cooccuranceSimilarityMatrix(data_map)
