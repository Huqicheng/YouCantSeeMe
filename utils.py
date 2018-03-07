import gensim
import pandas as pd
import numpy as np
from dataset import BXDataset
from scipy.sparse import csr_matrix
import json
import pickle

# train a word2vec model

#dataset = BXDataset()
#data_map = dataset.get_data('./book_crossing_dataset')
#users_new = data_map['users_new']
#location_split = users_new[['city','state','country']]
#temp_location_df = pd.concat([location_split.city, location_split.state,  location_split.country, location_split.state, location_split.city, location_split.country, location_split.city], axis=1)
#city = temp_location_df.fillna('n/a').values.tolist()
#model = gensim.models.Word2Vec(city, size=10, window=5, min_count=1, workers=4)
#model.save("./models/city_vects.model")

model= gensim.models.Word2Vec.load("./models/city_vects.model")

'''
    input is a str
    return: vector with shape(10,)
'''
def word2vect(word):
    return model[word]



def matrix2sparse(matrix,index_map):
    row = []
    col = []
    data = []
    for key in index_map.keys():
        row.append(key[0])
        col.append(key[1])
        data.append(matrix[key[0]][key[1]])
    return csr_matrix((data, (row, col)), shape=(matrix.shape[0], matrix.shape[0]))

def matrix2sparse2(index_map,shape):
    row = []
    col = []
    data = []
    for key in index_map:
        print key
        row.append(key[0])
        col.append(key[1])
        data.append(index_map[key])
    return csr_matrix((data, (row, col)), shape=shape)

def sparse2matrix(sparse):
    return sparse.toarray()


def save_obj(obj, path ):
    with open(path, 'wb') as f:
        f.write(json.dumps(obj))

def load_obj(path):
    with open(path, 'rb') as f:
        return json.loads(f.read())

if __name__ == '__main__':
#    matrix=[[1,2,3],[0,0,0],[0,0,0]]
#    matrix = np.array(matrix)
#    index_map={}
#    index_map[(0,0)] = 1
#    index_map[(0,1)] = 1
#    index_map[(0,2)] = 1
#
#    print matrix2sparse2(index_map,(3,3))
    print load_obj('./models/user_index.obj')
