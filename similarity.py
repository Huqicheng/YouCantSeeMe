import numpy as np
from dataset import BXDataset
from utils import matrix2sparse,sparse2matrix
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
    index_map = {}
    index_map_user_rating = {}
    for indice in users.index:
        print cnt,'/',users.shape[0]
        user = users.loc[indice]
        tmpCooccurance = np.zeros((item_num,item_num))
        # get intersections and traverse the intersections
        # query items bought by user
        item_user_rating = user_ratings[user_ratings['user_id']==user['user_id']]
        items_user_2 = item_user_rating['isbn']
        items_user = items_user_2.drop_duplicates()
        
        if items_user.shape[0]>200:
            continue
        for i in items_user.index:
            item1 = items_user.loc[i]
            idx1 = items_index[item1]
            index_map_user_rating[(cnt,idx1)] = item_user_rating[item_user_rating['isbn']==item1]['rating'].mean()
            for j in items_user.index:
                item2 = items_user.loc[j]
                if item1 == item2:
                    continue
                idx2 = items_index[item2]
                cooccurance[idx1][idx2] = cooccurance[idx1][idx2]+1
                if index_map.has_key((idx1,idx2)):
                    continue
                index_map[(idx1,idx2)] = 1
        cnt+=1
            
    return matrix2sparse(cooccurance,index_map),matrix2sparse(index_map_user_rating,shape=(user.shape[0],item_num))

def cooccuranceSimilarityMatrix(data_map,cooccur_path='./models/cooccurance.npy',user_item_path='./models/user_item.npy'):
    if os.path.exists(cooccur_path) == False:
        sparse_co,sparse_user_item = cooccuranceMatrix(data_map)
        np.save(cooccur_path,sparse_co)
        np.save(cooccur_path,sparse_user_item)
    
    cooccurance = np.load(cooccur_path)[()]
    item_user = np.load(user_item_path)[()]
    return cooccurance,user_item_path



def ToutiaoSimilarity(i,j,cooccurance):
    if i==j:
        return 1.0
    if cooccurance[i,:].sum()==0 or cooccurance[j,:].sum()==0:
        return 0.0
    return float(cooccurance[i][j])/float(cooccurance[i,:].sum()*cooccurance[j,:].sum())

def ToutiaoSimilarityMatrix(data_map,cooccur_path='./models/cooccurance.npy',similarity_path='./models/similarity.npy'):
    # model exists, then return it directly
    if os.path.exists(similarity_path) == True:
        similarityMatrix = np.load(similarity_path)[()]
        return sparse2matrix(similarity_path)
    # get cooccurance if it's existed
    if os.path.exists(cooccur_path) == False:
        sparse = cooccuranceMatrix(data_map)
        np.save(cooccur_path,sparse)
    cooccurance = sparse2matrix(np.load(cooccur_path)[()])
    item_num = cooccurance.shape[0]
    similarityMatrix = np.zeros((item_num,item_num))
    index_map = {}
    for i in range(item_num):
        for j in range(item_num-i):
            similarityMatrix[i][j] = similarityMatrix[j][i] = ToutiaoSimilarity(i,j,cooccurance)
            if similarityMatrix[i][j]!=0:
                idx1 = min(i,j)
                idx2 = max(i,j)
                index_map[(idx1,idx2)] = 1
    sparseMatrix = matrix2sparse(similarityMatrix,index_map)

    np.savetxt(similarity_path,sparseMatrix)
    return similarityMatrix




if __name__ == '__main__':
    dataset = BXDataset()
    
    print cooccuranceSimilarityMatrix(dataset.get_data('./book_crossing_dataset'))



