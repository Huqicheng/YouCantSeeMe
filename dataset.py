import pandas as pd
import numpy as np

class Dataset(object):
    def __init__(self):
        self.data_map = {}
        self.descriptions = {}
        pass

    def get_data(self,root_dir_path):
        self.load_original_data(root_dir_path)
        self.preprocessing()
        return self.data_map
    
    def load_original_data(self,root_dir_path):
        pass

    def preprocessing(self):
        pass

    def describe(self):
        pass


class BXDataset(Dataset):
    def __init__(self):
        super(BXDataset, self).__init__()

    def get_data_map(self):
        return self.data_map

    def load_original_data(self,root_dir_path):
        users_new = pd.read_csv(root_dir_path+'/users_new.csv', sep=';', encoding='latin-1',low_memory=False)
        users_w_ex_ratings = pd.read_csv(root_dir_path+'/users_w_ex_ratings.csv', sep=';', encoding='latin-1',low_memory=False)
        users_w_im_ratings = pd.read_csv(root_dir_path+'/users_w_im_ratings.csv', sep=';', encoding='latin-1',low_memory=False)
        items_wo_duplicates = pd.read_csv(root_dir_path+'/items_wo_duplicates.csv', sep=';', encoding='latin-1',low_memory=False)
        ratings_expl = pd.read_csv(root_dir_path+'/ratings_expl.csv', sep=';', encoding='latin-1',low_memory=False)
        ratings_impl = pd.read_csv(root_dir_path+'/ratings_impl.csv', sep=';', encoding='latin-1',low_memory=False)
        self.data_map = {
            'users_new':users_new,
            'users_w_ex_ratings':users_w_ex_ratings,
            'users_w_im_ratings':users_w_im_ratings,
            'items_wo_duplicates':items_wo_duplicates,
            'ratings_expl':ratings_expl,
            'ratings_impl':ratings_impl
        }

    '''
        one-hot encoding ........... impossible
        word2vect .................. i dont know
    '''
    def preprocessing(self):
        # load index of items to a map
        index_map = {}
        items = self.data_map['items_wo_duplicates']
        for i in range(items.shape[0]):
            item = items.loc[i]
            index_map[item['isbn']] = i
        self.data_map['item_index_map'] = index_map
        

    def describe(self):
        self.data_map = {
            'users_new':'Users dataframe without NaN values and split location strings or word embeddings.',
            'users_w_ex_ratings':'Users who have contributed at least one explicit rating.',
            'users_w_im_ratings':'Users who have contributed at least one implicit rating.',
            'items_wo_duplicates':'Items dataframe without double entries or NaN values.',
            'ratings_expl':'Dataframe with the explicit ratings.',
            'ratings_impl':'Dataframe with the implicit ratings'
        }
        print self.descriptions


if __name__ == '__main__':
    dataset = BXDataset()
    data_map = dataset.get_data('./book_crossing_dataset')
    items_user = data_map['users_w_ex_ratings']
