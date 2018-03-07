from recommender import ItemCFRecommender
from dataset import BXDataset
from utils import *
rec = ItemCFRecommender()

dataset = BXDataset()
data_map = dataset.get_data('./book_crossing_dataset')

#save_obj(data_map['item_index_map'],'./models/item_index.obj')
#save_obj(data_map['user_index_map'],'./models/user_index.obj')

# training
#recommender.fit(data_map)
#
#recommender.save('./models')


# testing
rec.load('./models')

rec.recommend(str(data_map['users_w_ex_ratings'].iloc[0]['user_id']))


