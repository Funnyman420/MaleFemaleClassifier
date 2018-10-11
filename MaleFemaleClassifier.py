import numpy as np
import pandas as pd



data = pd.read_csv("Greek_Names.csv")


del data['isFemale']

start = 2
end = 5


data = pd.DataFrame(data.Names.str.split('-').tolist(), index = data.isMale).stack()
data = data.reset_index()[[0,'isMale']]
data.columns = ['Names', 'isMale']

data = data.drop(data[data.Names.map(len)<2].index)

data = pd.concat(g for _, g in data.groupby('isMale') if len(g)>1)

data = data.sort_values(by='Names')

data = data.reset_index(drop=True)

temp = data[0:0]
final = data[0:0]
    
for i in range(len(data)):
    if i == data.index[-1]:
        temp = temp.append(data.iloc[i])
        temp = temp.mode()
        final = final.append(temp.iloc[0])
        temp = temp[0:0]
        break
    else:
        if data.iloc[i]['Names'] == data.iloc[i+1]['Names']:
            temp = temp.append(data.iloc[i])
        else:
            temp = temp.append(data.iloc[i])
            temp = temp.mode()
            final = final.append(temp.iloc[0])
            temp = temp[0:0]
final = final.reset_index(drop=True)

for n in range(start,end):
    final['Column ' + str(n)] = final['Names'].astype(str).str[-n:]



