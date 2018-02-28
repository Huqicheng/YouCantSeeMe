import pandas as pd
import numpy as np
import gensim
import tqdm   #to visualize loops' progress

# -*- coding: latin-1 -*-


## Import Data from csv
# read Users
u_cols = ['user_id', 'location', 'age']
users = pd.read_csv('bx/BX-Users.csv', sep=';', names=u_cols, encoding='latin-1',low_memory=False)

# read Books/items
i_cols = ['isbn', 'book_title' ,'book_author','year_of_publication', 'publisher', 'img_s', 'img_m', 'img_l']
items = pd.read_csv('bx/BX-Books.csv', sep=';', names=i_cols, encoding='latin-1',low_memory=False)

# read Ratings
r_cols = ['user_id', 'isbn', 'rating']
ratings = pd.read_csv('bx/BX-Book-Ratings.csv', sep=';', names=r_cols, encoding='latin-1',low_memory=False)

users = users.loc[1:]
users.reset_index(drop=True, inplace=True)

items = items.loc[1:,:]
items.reset_index(drop=True, inplace=True)
items.drop(['img_s','img_m','img_l'], axis=1, inplace=True)

ratings = ratings.loc[1:,:]
ratings.reset_index(drop=True, inplace=True)


#User Dataframe

users.age = users.age.astype(float)
users.user_id = users.user_id.astype(int)
users.describe(include=[object, int, float])
users.loc[(users.age>99) | (users.age<5),'age'] = np.nan
users.age.fillna(users.age.mean()).describe()
# create a normal disgtribution pd.Series to fill Nan values with
temp_age_series = pd.Series(np.random.normal(loc=users.age.mean(), scale=users.age.std(), size=users.user_id[users.age.isnull()].count()))
print("Statistics of values in \'users.age\'\n",users.age.describe(),"\n")
print("Statistics of values we are going to use to fill NaN \n",temp_age_series.describe(),"\n")
print("Negative values in \'temp_age_seires\':", temp_age_series[temp_age_series<0].count(),"\n")
print("As we can see the destribution doesnt change a lot. There are some negative values thought (around 600 of them).\n")

# take the abs value of temp_age_series
pos_age_series=np.abs(temp_age_series)

# sort users Df so as NaN values in age to be first and reset index to match with index of pos_age_series. Then use fillna()
users = users.sort_values('age',na_position='first').reset_index(drop=True)
users.age.fillna(pos_age_series, inplace = True)  

# replace values < 5 with the mean(). Round values and convert them to int. 
users.loc[users.age<5, 'age'] = users.age.mean()
users.age = users.age.round().astype(int)
#Sort users based on user_id so as to be the same as before
users = users.sort_values('user_id').reset_index(drop=True)
print(users.age.describe(),"\n")
users.head()
users.location.head()
location_split=users.location.str.split(', ', n=2, expand=True)
location_split.columns=['city', 'state', 'country']
location_split.describe(include=[object])
location_split.loc[location_split.state==',', ['state', 'country']] = 'other'
location_split.loc[location_split.country==',', ['country']] = 'other'
location_split.loc[(location_split.state=='\\n/a\\"') | (location_split.state=='') | (location_split.state=='*') | (location_split.state=='n.a'), ['state']] = 'n/a'
location_split.state.fillna('other', inplace=True)
location_split.fillna('n/a', inplace=True)
temp_location_df = pd.concat([location_split.city, location_split.state,  location_split.country, location_split.state, location_split.city, location_split.country, location_split.city], axis=1)
location_list = temp_location_df.fillna('n/a').values.tolist()
print location_list
n = 10
model = gensim.models.Word2Vec(location_list, size= n, window=3, min_count=1, workers=4)
print ('UK is to Milton Keynes what Greece is to : ')
model.most_similar(positive=['greece','united kingdom'], negative=['milton keynes'], topn=20)
rightchoice=['1','2']
# choice = input("Choose \'1\' to skip this step or \'2\' to construct the \'location_vec\' DataFrame.")
# while choice not in rightchoice:
#     choice = input("Wrong input. \n Insert a number. Either 1 or 2")
# if choice=='1':
#     print ('Skipping operations')
# else:
#     zipp = list(zip(model.wv.index2word, model.wv.syn0))
#     vectors = np.zeros((location_split.shape[0],3*n))
#     for i in tqdm.tqdm_notebook(range(location_split.shape[0])):
#         vectors[i, 0:20] = [j[1][0] for j in zipp if j[0] == location_split.loc[i, 'city']]
#         vectors[i,20:40] = [j[1][0] for j in zipp if j[0] == location_split.loc[i, 'state']]
#         vectors[i,40:60] = [j[1][0] for j in zipp if j[0] == location_split.loc[i, 'country']]
#     col=[]
#     for i in range(20):
#         col.append('city_'+ str(i))
#     for i in range(20):
#         col.append('state_'+ str(i))
#     for i in range(20):
#         col.append('country_'+ str(i))

#     location_vec = pd.DataFrame(vectors, columns = col)
if 'location_vec' in globals():
    users_new = pd.concat([users.user_id, location_vec , users.age], axis=1)    
else:
    users_new = pd.concat([users.user_id, location_split , users.age], axis=1)
users_new.head()

#Item Dataframe
items = pd.read_csv('BX_Books_correct.csv', sep=';', names=i_cols, encoding='latin-1',low_memory=False)
items = items.loc[1:]
items.reset_index(drop=True, inplace=True)
items.drop(['img_s','img_m','img_l'], axis=1, inplace=True)
items.year_of_publication = items.year_of_publication.astype(int)
items.describe(include =[object, int])
items.head()
print ("Items with NaN values in \"book_author\": \n", items.isbn[items.book_author.isnull()],"\n")
print ("Items values in \"publisher\": \n", items.isbn[items.publisher.isnull()])
items.loc[187701,'book_author'] = "n/a"
items.loc[[128897, 129044],'publisher'] = "NovelBooks, Inc"
print('Items with (year_of_publication > 2010):', items.year_of_publication[items.year_of_publication>2010].count(),'\n')
print('value_counts of items with (year_of_publication < 1500): \n', items.year_of_publication[items.year_of_publication<1500].value_counts())
items.loc[(items.year_of_publication>2010)|(items.year_of_publication<1000),'year_of_publication'] = np.nan
print(items.describe(),'\n')
print(items.year_of_publication.fillna(round(items.year_of_publication.mean())).describe())
items.year_of_publication.fillna(round(items.year_of_publication.mean()),inplace=True)
items.year_of_publication = items.year_of_publication.astype(int)


#duplicate entries
items_wo_duplicates = items.drop_duplicates(['book_title', 'book_author'])
items_wo_duplicates.describe(include=[object,int])
#Rating
ratings_new = ratings[ratings.isbn.isin(items.isbn)]
ratings_new.describe()
ratings_new.loc[:,'rating'] = ratings_new.rating.astype(int)
print(ratings_new.rating.value_counts(sort=False))
ratings_new.describe(include=[object,int])
choice = input("Choose \'1\' to import the ratings_wo_duplicates file or \'2\' to construct it again ")
while choice not in rightchoice:
    choice = input("Wrong input. \n Insert a number. Either 1 or 2")

if choice == '1':
    ratings_wo_duplicates=pd.read_csv('ratings_wo_duplicates.csv', sep=';', names=r_cols, encoding='latin-1', low_memory=False )
    print('Done')
elif choice == '2':
    choice = input("Choose \'1\' to iterate through all items or \'2\' if this operation was interupted and you would like to continue from the last checkpoint.")
    while choice not in rightchoice:
        choice = input("Wrong input. \n Insert a number. Either 1 or 2")
    
    if choice == '1':
        nof = 0
        ratings_wo_duplicates = ratings_new
        count=0
    else:
        nof = int(input('Please insert the number of processed and stored items.'))
        ratings_wo_duplicates=pd.read_csv('ratings_wo_duplicates.csv', sep=';', names=r_cols, encoding='latin-1', low_memory=False )
        count= nof
    
    # create a series with all the duplicates (including the first occurance) to iterate
    temp=items[(items.duplicated(['book_title', 'book_author'],keep=False))][nof:]
    
    for t in tqdm.tqdm_notebook(temp['book_title']):
        x = list( items[items['book_title']==t].isbn)
        count+=1 
        for i in range(1, len(x)):
            #replace all entries in x list with x[0] (the isbn we kept in items_wo_duplicates)
            ratings_wo_duplicates.loc[ratings_wo_duplicates.isbn==x[i],'isbn'] = x[0]

        if count%2000==0:
            ratings_wo_duplicates.to_csv('ratings_wo_duplicates.csv',';')
            print(count ,' duplicate items ratings processed and stored')
            
    ratings_wo_duplicates.to_csv('ratings_wo_duplicates.csv',';')
    print('Done')


ratings_wo_duplicates = ratings_wo_duplicates.loc[1:]
ratings_wo_duplicates.reset_index(drop=True, inplace=True)
ratings_wo_duplicates.rating = ratings_wo_duplicates.rating.astype(int)
# print('\nAnd to make sure that the procedure was carried out smoothly,')
# print('No of duplicates in \"ratings_wo_duplicates\" :',ratings_wo_duplicates.isbn[ratings_wo_duplicates.isbn.isin(items[items.duplicated(['book_title', 'book_author'])].isbn)].count())
ratings_expl = ratings_wo_duplicates[ratings_wo_duplicates.rating != 0]
ratings_impl = ratings_wo_duplicates[ratings_wo_duplicates.rating == 0]
# print(ratings_expl.describe(include=[object,int]),'\n')
# print(ratings_impl.describe(include=[object,int]))
users_w_ex_ratings = users_new[users_new.user_id.isin(ratings_expl.user_id)]
users_w_im_ratings = users_new[users_new.user_id.isin(ratings_impl.user_id)]
items_w_ratings = items_wo_duplicates[items_wo_duplicates.isbn.isin(ratings_wo_duplicates.isbn)]


#save files
users_new.to_csv('../users_new.csv',';',encoding='latin-1')
users_w_ex_ratings.to_csv('../users_w_ex_ratings.csv',';',encoding='latin-1')
users_w_im_ratings.to_csv('../users_w_im_ratings.csv',';',encoding='latin-1')
items_wo_duplicates.to_csv('../items_wo_duplicates.csv',';',encoding='latin-1')
ratings_wo_duplicates.to_csv('../ratings_wo_duplicates.csv',';',encoding='latin-1')
ratings_expl.to_csv('../ratings_expl.csv',';',encoding='latin-1')
ratings_impl.to_csv('../ratings_impl.csv',';',encoding='latin-1')
