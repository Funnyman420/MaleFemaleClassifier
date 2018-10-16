import pandas as pd
import seaborn as sns
import numpy as np
import unicodedata

def clearMinorities (data):
    toDelete = []
    
    for i in range(len(data)-1):
        if data.iloc[i]['Names'] == data.iloc[i+1]['Names']:
            if data.iloc[i]['Frequency'] > data.iloc[i+1]['Frequency']:
                toDelete.append(data.index[i+1])
            else:
                toDelete.append(data.index[i])
    return toDelete

def encode(c) : return ord(c) - 785
def decode(i) : return chr(i + 785)

data = pd.read_csv("Greek_Names.csv",sep=',')
del data['isFemale']

data = pd.DataFrame(data.Names.str.split('-').tolist(), index = data.isMale).stack()
data = data.reset_index()[[0,'isMale']]
data.columns = ['Names', 'isMale']
data = data.drop(data[data.Names.map(len)<2].index)
data = pd.concat(g for _, g in data.groupby('isMale') if len(g)>1)


data['Frequency'] = data.groupby(['Names', 'isMale'])[['Names']].transform('count')

data = data.sort_values(by='Names')

data.drop_duplicates(keep='first', inplace=True)
data.reset_index(drop=True,inplace = True)

toRemoveList = clearMinorities(data)

data.drop(data.index[toRemoveList],inplace=True)

data.drop('Frequency',axis=1,inplace=True)

data = data.reset_index(drop=True)

start = 2
end = 4

for n in range(start,end):
    data['Column ' + str(n)] = data['Names'].astype(str).str[-n:]

data.loc[data['isMale'] == 0, 'isMale'] = 'Female'
data.loc[data['isMale'] == 1, 'isMale'] = 'Male'
data = data.rename(columns={'isMale' : 'Gender', 'Column 2' : 'Suffix 2', 'Column 3' : 'Suffix 3'})

data['Frequency'] = 1

pivot = pd.pivot_table(data, values = 'Frequency', index='Suffix 2', columns='Gender', aggfunc='count').fillna(0)

pivot.reset_index(inplace=True)
sufvalues2 = pivot.values

suf2 = pd.DataFrame({'Suffix 2' : sufvalues2[:,0],'Female':sufvalues2[:,1],'Male':sufvalues2[:,2]})

list = []
for s in suf2['Suffix 2']:
        list.append([encode(c) for c in s])
#[("%d" % encode(c) for c in s) for s in suf2['Suffix 2']]

print(list)
#se = pd.Series(list[:])
#suf2 = suf2.reset_index(drop=True)
#suf2['ASCII 1'] = se.values
#print(suf2)

#suf2.to_csv('suffix2.csv', sep=',')
"""
pivot = pd.pivot_table(data, values = 'Frequency', index='Suffix 3', columns='Gender', aggfunc='count').fillna(0)
pivot.reset_index(inplace=True)
sufvalues3 = pivot.values
suf3 = pd.DataFrame({'Suffix 3' : sufvalues3[:,0],'Female':sufvalues3[:,1],'Male':sufvalues3[:,2]})
suf3.to_csv('suffix3.csv', sep=',')
"""