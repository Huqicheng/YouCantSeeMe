import numpy as np
from dataset import BXDataset
from utils import matrix2sparse
import sys,os
def cos_sim(x, y):
    assert len(x) == len(y)
    return x.dot(y) / np.sqrt(np.square(x).sum()) / np.sqrt(np.square(y).sum())


def euclidea_sim(x,y):
    assert len(x) == len(y)
    dis = np.linalg.norm(x-y)
    sim = 1/(1+dis)
    return sim

def jaccard_sim(x,y):
    assert len(x) == len(y)
    x,y = np.array(x).astype(bool),np,array(y).astype(bool)
    return sum(x*y)/sum(x+y)

'''
calculate similarity matrix
data is a matrix, one row as one sample
similarity is the specific similarity function, default as cosine similarity
'''
def similarityMatrix(data,similarity=cos_sim):
    sampleN = data.shape[0]
    simMatrix = np.zeros(shape=(sampleN,sampleN))
    for i in range(sampleN):
        for j in range(sampleN):
            if simMatrix[j][i] == 0:
                simMatrix[i][j] = similarity(data[i],data[j])
            else:
                simMatrix[i][j] = simMatrix[j][i]
    return simMatrix

def cooccuranceMatrix(data_map):
    # get necessary dataframes from map
    items = data_map['items_wo_duplicates']
    users = data_map['users_w_ex_ratings']
    user_ratings = data_map['ratings_expl']
    items_index = data_map['item_index_map']
    # get quantity of items
    item_num = items.shape[0]
    # initiate the cooccuranceMatrix
    # the index refers to the row number in data_map['items_wo_duplicates']
    cooccurance = np.zeros((item_num,item_num))
    # traverse all of users
    print users.shape
    
    progress = 0
    cnt = 0
    batch = users.shape[0]/1000
    
    for indice in users.index:
        cnt+=1
        print cnt,'/',users.shape[0]
        user = users.loc[indice]
        tmpCooccurance = np.zeros((item_num,item_num))
        # get intersections and traverse the intersections
        # query items bought by user
        items_user_2 = user_ratings[user_ratings['user_id']==user['user_id']]['isbn']
        items_user = items_user_2.drop_duplicates()
        if items_user.shape[0]>200:
            continue
        for i in items_user.index:
            item1 = items_user.loc[i]
            idx1 = items_index[item1]
            for j in items_user.index:
                item2 = items_user.loc[j]
                if item1 == item2:
                    continue
                idx2 = items_index[item2]
                cooccurance[idx1][idx2] = cooccurance[idx1][idx2]+1
#        if cnt==batch:
#            cnt=0
#            sys.stdout.write('#')
#            sys.stdout.flush()
    return cooccurance


def ToutiaoSimilarity(i,j,cooccurance):
    if i==j:
        return 1.0
    return float(cooccurance[i][j])/float(cooccurance[i,:].sum()*cooccurance[j,:].sum())

def ToutiaoSimilarityMatrix(data_map,cooccur_path='./models/cooccurance.npy',similarity_path='./models/similarity.npy'):
    # model exists, then return it directly
    if os.path.exists(similarity_path) == True:
        similarityMatrix = np.loadtxt(similarity_path)
        return similarity_path
    # get cooccurance if it's existed
    if os.path.exists(cooccur_path) == False:
        cooccurance = cooccuranceMatrix(data_map)
        sparse = matrix2sparse(cooccurance)
        np.save(cooccur_path,sparse)
#    cooccurance = np.loadtxt(cooccur_path)
#    item_num = cooccurance.shape[0]
#    similarityMatrix = np.zeros((item_num,item_num))
#    for i in range(item_num):
#        for j in range(item_num-i):
#            similarityMatrix[i][j] = similarityMatrix[j][i] = ToutiaoSimilarity(i,j,cooccurance)
#    np.savetxt(similarity_path,similarityMatrix)
#    return similarityMatrix




if __name__ == '__main__':
    dataset = BXDataset()
    
    data_map = dataset.get_data('./book_crossing_dataset')
    ToutiaoSimilarityMatrix(data_map)


