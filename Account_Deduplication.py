import pandas as pd
import nltk.data
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import numpy as np
import numpy as np
from nltk.tokenize import word_tokenize
import torch
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
!pip install geopy
!pip install python-Levenshtein==0.12.0
!pip install jarowinkler

df = pd.read_excel('Input file.xlsx')

df2 = df.loc[:,['Account Name','Billing Country','Billing State/Province','Billing City','Billing Street','Billing Zip/Postal Code']]


df2 = df.loc[:,['Account Name','Billing Country','Billing State/Province','Billing City','Billing Street',\
                'Billing Zip/Postal Code']]
df_count= pd.DataFrame()

df_count['Entity'] = ''
df_count['Percent'] = ''
df_count['Number'] = ''

num_records = len(df2)

df2 = df2.iloc[0:num_records,:]
df2 = df2.astype(str).apply(lambda x:x.str.lower())
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
count = 0
flag = 0
stop_words = []
stop_words = set(stop_words)

df2['Account ID'] = df['Account ID']
def remove_stop_words(text):
    global df_count
    global flag
    global stop_words
  
    global count
    text2 = ''
    if(len(df_count)==0):
        stop_words = set(stopwords.words('english'))
  
    else:
  
        if(flag ==0):
            for count in range(len(df_count)):
                if(df_count.loc[count, 'Number']<100):
                    flag = 1
                    break
        
        
        stop_words = set(df_count.loc[0:count-1,'Entity'])
    
    
        
    word_tokens = word_tokenize(text)
 
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
            text2 += w + ' '

    text2 = text2.strip()
    return text2

df3 = df2.copy(deep = True)
df2['Account Name'] = df2['Account Name'].apply(remove_stop_words)
df2['Billing Street'] = df2['Billing Street'].apply(remove_stop_words)
df2 = df2.astype(str).replace("[\'\".,()*+&\/\-\\\+\!\%:;?]","")
#df2=df3

print("Stop words (1st time) are...", stop_words)
df_count['Entity'] = df2['Account Name'].str.split(expand=True).stack().value_counts().index
df_count['Number'] = list(df2['Account Name'].str.split(expand=True).stack().value_counts().values)
sum1 = df2['Account Name'].str.split(expand=True).stack().value_counts().sum()
df_count['Percent'] = list((df2['Account Name'].str.split(expand=True).stack().value_counts()/sum1).values)


df3['Account Name'] = df3['Account Name'].apply(remove_stop_words)
df3['Billing Street'] = df3['Billing Street'].apply(remove_stop_words)
df3 = df3.astype(str).replace("[\'\".,()*+&\/\-\\\+\!\%:;?]","")
print("Stop words (2nd time) are...", stop_words)
#df2=df3

df_lookup = df.loc[:, ['Account ID', 'Account Name']]
df_lookup.head()
df2 = pd.merge(df2,df_lookup, on = 'Account ID', how = 'left')
df2.rename(columns = {'Account Name_x':'Account Name'}, inplace = True)


stop_words2 = []
for item in stop_words:
    if len(item)>1:
        stop_words2.append(item)

stop_words2 = set(stop_words)
print(stop_words2)
stop_words = stop_words2



import pandas as pd
import Levenshtein

from jarowinkler import *

df3 = df2
len_df3 = len(df3)
score = 0
score2= 0
index = 0
df3['Address_All'] = ''

for j in range(0, len(df3)):
    df3.loc[j,'Address_All'] = str(df3.loc[j,'Billing Country']) + ' '+ str(df3.loc[j,'Billing State/Province'])\
+ ' '+  str(df3.loc[j,'Billing City']) + ' '+str(df3.loc[j,'Billing Street'])\
+ ' '+ str(df3.loc[j,'Billing Zip/Postal Code'])

df_accounts = pd.DataFrame()
df_accounts['Id1'] = ''
df_accounts['Name1'] = ''
df_accounts['Id2'] = ''
df_accounts['Name2'] = ''
df_accounts['Original Name1'] = ''
df_accounts['Original Name2'] = ''
'''df_accounts2['Name1'] = ''
df_accounts2['Name2'] = '''''


for i in range(0, len_df3):
    print("I am in account number..", i)
    for j in range( i+1, len_df3):
        '''df_accounts2.loc[index, 'Name1'] = df3.loc[i,'Account Name']
        df_accounts2.loc[index, 'Name2'] = df3.loc[j,'Account Name']'''
        temp1 = df3.loc[i, 'Account Name']
        temp2 = df3.loc[j,'Account Name']
        for item in stop_words:
            if(any(item == word for word in temp1.split()) and any(item == word for word in temp2.split())):
                temp1 = temp1.replace(item, ' ').strip()
                temp2 = temp2.replace(item, ' ').strip()
                #print(f"temp1 is {temp1} and temp2 is {temp2} and item is {item}")
                
        score  =  jaro_similarity(temp1, temp2)
        if(score > 0.91 and df3.loc[i, 'Account Name'] !='' and df3.loc[j,'Account Name']!= ''):
            #print(f"temp1 is {temp1} and temp2 is {temp2}")
            #print(f"original accounts are {df3.loc[i, 'Account Name_y']} and {df3.loc[j, 'Account Name_y']}")
            df_accounts.loc[index, 'Id1'] = df3.loc[i, 'Account ID']
            df_accounts.loc[index, 'Id2'] = df3.loc[j, 'Account ID']
            df_accounts.loc[index, 'Name1'] = temp1
            df_accounts.loc[index, 'Name2'] = temp2
            df_accounts.loc[index, 'Original Name1'] = df3.loc[i, 'Account Name_y']
            df_accounts.loc[index, 'Original Name2'] = df3.loc[j, 'Account Name_y']
            df_accounts.loc[index, 'Address1'] = df3.loc[i, 'Address_All']
            df_accounts.loc[index, 'Address2'] = df3.loc[j, 'Address_All']

            df_accounts.loc[index, 'Similarity_Name'] = score
            score2  =  jaro_similarity(df3.loc[i, 'Address_All'], df3.loc[j,'Address_All'])
            df_accounts.loc[index, 'Similarity_Address'] = score2
        index +=1

