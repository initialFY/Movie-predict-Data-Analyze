import pandas as pd
import sys
import ast
import json
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
import warnings 
warnings.filterwarnings('ignore')
if not len(sys.argv) == 3:
    print("lack of path1 or path2")
    sys.exit()
df = pd.read_csv(sys.argv[1]) #read training set
test = pd.read_csv(sys.argv[2]) #test set
df2 = df[['cast', 'crew', 'budget', 'original_language', 'release_date', 'runtime']]
test2 = test[['cast', 'crew', 'budget', 'original_language', 'release_date', 'runtime']]
part1_test = df[['revenue']]
result = df['cast']
#get all_result,test_result
all_result = []
for i in result:
    result = ast.literal_eval(i)
    all_result.append(result[0]['name'])
#print(len(list(set(all_result))))
test_result = test['cast']
test_all_result = []
for i in test_result:
    test_result = ast.literal_eval(i)
    test_all_result.append(test_result[0]['name'])
all_result=list(set(all_result))
test_all_result=list(set(test_all_result))
#print(len(list(set(test_all_result))))
#change cast
df2_1=df2.copy()
test2_1=test2.copy()
for i in range(len(df2['cast'])):
    target_cast = ast.literal_eval(df2['cast'][i])
    #print(target_cast[0]['name'])
    #df2_1['cast'][i] = target_cast[0]['name']
    df2_1.loc[i,'cast'] = target_cast[0]['name']
for i in range(len(test2['cast'])):
    test_target_cast = ast.literal_eval(test2['cast'][i])
    test2_1.loc[i,'cast'] = test_target_cast[0]['name']
#get director_result,test_director_result
# director_result=[]
# for i in range(len(df2['crew'])):
#     target_crew = ast.literal_eval(df2['crew'][i]) 
#     for j in target_crew:
#         if j['job'] == 'Director':
#             director_result.append(j['name'])
#             df2['crew'][i] = j['name'] 
# test_director_result=[]            
# for i in range(len(test2['crew'])):
#     test_target_crew = ast.literal_eval(test2['crew'][i]) 
#     for j in test_target_crew:
#         if j['job'] == 'Director':
#             test_director_result.append(j['name'])
#             test2['crew'][i] = j['name'] 
# director_result=list(set(director_result))
# test_director_result=list(set(test_director_result))
#print(len(director_result),len(test_director_result))
#change crew
df2_2=df2_1.copy()
test2_2=test2_1.copy()
director_result=[]
for i in range(len(df2_1['crew'])):
    target_crew = ast.literal_eval(df2['crew'][i]) 
    for j in target_crew:
        if j['job'] == 'Director':
            director_result.append(j['name'])
            df2_2.loc[i,'crew'] = j['name']
            #df2['crew'][i] = j['name'] 
test_director_result=[]            
for i in range(len(test2_1['crew'])):
    test_target_crew = ast.literal_eval(test2['crew'][i]) 
    for j in test_target_crew:
        if j['job'] == 'Director':
            test_director_result.append(j['name'])
            test2_2.loc[i,'crew'] = j['name'] 
director_result=list(set(director_result))
test_director_result=list(set(test_director_result))

#change cast to num         
df2_3 = df2_2.copy()
test2_3 = test2_2.copy()
for i in range(0,len(df2['cast'])):
    #print(df2['cast'][i],all_result.index(df2['cast'][i])+1)
    #df2_2['cast'][i]=all_result.index(df2['cast'][i])+1
    df2_3.loc[i,'cast'] = all_result.index(df2_2['cast'][i])+1
for i in range(0,len(test2['cast'])):
    #test2_2['cast'][i]=test_all_result.index(test2['cast'][i])+1
    test2_3.loc[i,'cast'] = test_all_result.index(test2_2['cast'][i])+1
#change crew to num
df2_4 = df2_3.copy()
test2_4 = test2_3.copy()
for i in range(0,len(df2['crew'])):
    #print(df2['cast'][i],all_result.index(df2['cast'][i])+1)
    df2_4.loc[i,'crew']=director_result.index(df2_3['crew'][i])+1
for i in range(0,len(test2['crew'])):
    test2_4.loc[i,'crew']=test_director_result.index(test2_3['crew'][i])+1
#get lan_result,test_lan_result
lan_result=[]
for i in range(len(df2['original_language'])):
    target_lan = df2['original_language'][i]
    lan_result.append(target_lan) 
test_lan_result=[]
for i in range(len(test2['original_language'])):
    test_target_lan = test2['original_language'][i]
    test_lan_result.append(test_target_lan)  
lan_result=list(set(lan_result))
test_lan_result=list(set(test_lan_result))
#change language to num
df2_5 = df2_4.copy()
test2_5 = test2_4.copy()
for i in range(0,len(df2['original_language'])):
    #print(df2['cast'][i],all_result.index(df2['cast'][i])+1)
    df2_5.loc[i,'original_language']=lan_result.index(df2_4['original_language'][i])+1
for i in range(0,len(test2['original_language'])):
    test2_5.loc[i,'original_language']=test_lan_result.index(test2_4['original_language'][i])+1
#simply df2,test2
df3 = df2_5[['cast','crew', 'budget', 'original_language', 'runtime']]
test3 = test2_5[['cast','crew', 'budget', 'original_language', 'runtime']]
#get set
part1_test = df[['revenue']]

#p1 op
part1 = LinearRegression().fit(df3,part1_test)
result = part1.predict(test3)
movie_id = test['movie_id']
df5 = pd.DataFrame()
df5['movie_id'] = test['movie_id']
df5['predicted_revenue'] = result 
df5.to_csv("z5223014.PART1.output.csv")

#p2 op
part2_test = df[['rating']]
part2 = KNeighborsClassifier(n_neighbors=3) 
part2.fit(df3,part2_test)
knn_result = part2.predict(test3)
df6 = pd.DataFrame()
df6['movie_id'] = test['movie_id']
df6['predicted_rating'] = knn_result 
df6.to_csv("z5223014.PART2.output.csv")

#p1 p2 sm
from sklearn.metrics import *

MSR = mean_squared_error(test.revenue,result)

from scipy.stats import pearsonr
PC = pearsonr(test.revenue,result.reshape(400))
df7 = pd.DataFrame()
df7['zid'] = ['z5223014']
df7['MSR'] = [MSR]
df7['correlation'] = PC[0]
df7.to_csv("z5223014.PART1.summary.csv")


p_s=precision_score(test.rating,knn_result,average='micro')
r_s=recall_score(test.rating,knn_result,average='macro')
a_s=accuracy_score(test.rating,knn_result)

df8 = pd.DataFrame()
df8['zid'] = ['z5223014']
df8['average_precision'] = [p_s]
df8['average_recall'] = [r_s]
df8['accuracy'] = [a_s]
df8.to_csv("z5223014.PART2.summary.csv")