import gensim
import pandas as pd
from dataset import BXDataset
from scipy.sparse import csr_matrix

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



def matrix2sparse(matrix):
    row = []
    col = []
    data = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]-i):
            if matrix[i][j] != 0:
                row.append(i)
                col.append(j)
                data.append(matrix[i][j])
    return csr_matrix((data, (row, col)), shape=(matrix.shape[0], matrix.shape[0]))

def sparse2matrix(sparse):
    return sparse.toarray()
