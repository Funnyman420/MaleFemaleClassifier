import pandas as pd
import seaborn as sns
import numpy as np
import unicodedata

#Decides what Rows of the grouped DataFrame are to be deleted.Helps with the speed of the script
def clearMinorities (dataframe,column):
    toDelete = []
    for i in range(len(dataframe)-1):
        if dataframe.iloc[i][str(column)] == dataframe.iloc[i+1][str(column)]:
            if dataframe.iloc[i]['Frequency'] > dataframe.iloc[i+1]['Frequency']:
                toDelete.append(dataframe.index[i+1])
            else:
                toDelete.append(dataframe.index[i])
    return toDelete


#Splits the DataFrame into the desired character and stacks the 2 resulting elements into the DataFrame
def splitToCharacter(dataframe,symb):
    dataframe = pd.DataFrame(dataframe.Names.str.split(symb).tolist(), index = dataframe.isMale).stack()
    dataframe = dataframe.reset_index()[[0,'isMale']]

    return dataframe

#Clears names with length smaller than or equal to 2. Helps to keep data clean after the method splitToCharacter
def clearSmallNames (dataframe):

    dataframe = dataframe.drop(data[data.Names.map(len)<2].index)
    dataframe = pd.concat(g for _, g in dataframe.groupby('isMale') if len(g)>1)
    
    return dataframe


#Voting Method to desired DataFrame
def keepTheMostFrequentName(dataframe, nameColumn, otherColumn):
    
    dataframe['Frequency'] = dataframe.groupby([nameColumn, otherColumn])[[nameColumn]].transform('count')
    dataframe = dataframe.sort_values(by=nameColumn)
    dataframe.drop_duplicates(keep='first', inplace=True)
    dataframe.reset_index(drop=True,inplace = True)
    toRemoveList = clearMinorities(dataframe,nameColumn)
    dataframe.drop(dataframe.index[toRemoveList],inplace=True)
    dataframe.drop('Frequency',axis=1,inplace=True)
    dataframe = dataframe.reset_index(drop=True)

    return dataframe


#Changes the values of a column. Insert the current value that you want to change and then the desired value
def changeValuesOfColumn(dataframe,column,currentvalue,desirablevalue):
    dataframe.loc[dataframe[column] == currentvalue, column] = desirablevalue
    
    return dataframe


#Makes new Columns accoding to how many characters of the name you want to keep
def makeNewColumns(dataframe,start,end):
    for n in range(start,end):
        dataframe['Column ' + str(n)] = dataframe['Names'].astype(str).str[-n:]

    return dataframe


#Calculates the Suffix Values of desired Suffix Column
def calcSufValues(dataframe, pivotindex):
    pivot = pd.pivot_table(dataframe, values = 'Frequency', index=pivotindex, columns='Gender', aggfunc='count').fillna(0)
    pivot.reset_index(inplace=True)

    return pivot.values

#Encoding to ASCII format
def encode(c) : return ord(c) - 785
def decode(i) : return chr(i + 785)


#Start of Main
data = pd.read_csv("Greek_Names.csv",sep=',')
del data['isFemale']

data = splitToCharacter(data,'-')
#Renaming the Columns of DataFrame
data.columns = ['Names', 'isMale']

data = clearSmallNames(data)
data = keepTheMostFrequentName(data, 'Names', 'isMale')
data = makeNewColumns(data,2,4)
data = changeValuesOfColumn(data,'isMale',0,'Female')
data = changeValuesOfColumn(data,'isMale',1,'Male')

#Renaming some Columns of Dataframe to make the DataFrame more undestandable. Also creates Column Frequency to help with the Pivot Table
data = data.rename(columns={'isMale' : 'Gender', 'Column 2' : 'Suffix 2', 'Column 3' : 'Suffix 3'})
data['Frequency'] = 1

sufvalues2 = calcSufValues(data,'Suffix 2')

#Creating DataFrame filled with Suffix 2, Frequency of Male, Frequency of Female and ASCII values and outputs a CSV file with said DataFrame
suf2 = pd.DataFrame({'Suffix 2' : sufvalues2[:,0],'Female':sufvalues2[:,1],'Male':sufvalues2[:,2]})
suf2['ASCII 1'] = ["".join("%d" % encode(c) for c in s)[:3] for s in suf2['Suffix 2']]
suf2['ASCII 2'] = ["".join("%d" % encode(c) for c in s)[3:] for s in suf2['Suffix 2']]
suf2.to_csv('suffix2.csv', sep=',')

#Creating DataFrame filled with Suffix 3, Frequency of Male, Frequency of Female and ASCII values and outputs a CSV file with said DataFrame
sufvalues3 = calcSufValues(data,'Suffix 3')
suf3 = pd.DataFrame({'Suffix 3' : sufvalues3[:,0],'Female':sufvalues3[:,1],'Male':sufvalues3[:,2]})
suf3['ASCII 1'] = ["".join("%d" % encode(c) for c in s)[:3] for s in suf3['Suffix 3']]
suf3['ASCII 2'] = ["".join("%d" % encode(c) for c in s)[3:6] for s in suf3['Suffix 3']]
suf3['ASCII 3'] = ["".join("%d" % encode(c) for c in s)[-3:] for s in suf3['Suffix 3']]
suf3.to_csv('suffix3.csv', sep=',')
