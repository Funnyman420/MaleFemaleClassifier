import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import confusion_matrix, classification_report
from johnny_wordie import JohnnyWordie

# Encoding to ASCII format
def encode(c): return ord(c) - 785


def decode(i): return chr(i + 785)


# Makes new Columns accoding to how many characters of the name you want to keep
def make_new_columns(data_frame, start, end):
    for n in range(start, end):
        data_frame['Column ' + str(n)] = data_frame['Names'].astype(str).str[-n:]

    return data_frame


data = pd.read_csv('CleanNames.csv', sep=',', index_col='Unnamed: 0')
data['Names'] = data['Names'].str.lower()

data = make_new_columns(data, 2, 3)

data['ASCII 1'] = ["".join("%d" % encode(c) for c in s)[:3] for s in data['Column 2']]
data['ASCII 2'] = ["".join("%d" % encode(c) for c in s)[3:] for s in data['Column 2']]
print(data)
x = data.iloc[:, 3:5]
print(x)
y = data.iloc[:, 1]
print(y)

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.3, random_state=4)

print(xtrain[:5])

model = DecisionTreeClassifier(criterion='gini', min_samples_split=20, min_samples_leaf=1)
model.fit(xtrain, ytrain)
ypred = model.predict(xtest)
print(confusion_matrix(ytest, ypred))
print(classification_report(ytest, ypred))

name_data = JohnnyWordie('Spells.txt')
x = name_data.data.iloc[:, 4:6]
name_data.data['gender'] = model.predict(x)
print(name_data.data)
del name_data.data['ASCII 1']
del name_data.data['ASCII 2']
del name_data.data['Suffix 2']
name_data.data.to_csv('names_genders.csv')


