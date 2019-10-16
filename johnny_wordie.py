import pandas as pd
pd.set_option('display.max_columns', 500)

# Encoding to ASCII format
def encode(c): return ord(c) - 785


def decode(i): return chr(i + 785)


def make_new_columns(data_frame, start, end):
    for n in range(start, end):
        data_frame['Suffix ' + str(n)] = data_frame['full_name_1'].astype(str).str[-n:]

    return data_frame


class JohnnyWordie:
    def __init__(self, text):
        self.data = pd.read_csv(str(text), delimiter=';', header=None)
        self.data.columns = ['full_name_1', 'full_name_2', 'broken_name']
        self.data = make_new_columns(self.data, 2, 3)
        self.data['ASCII 1'] = ["".join("%d" % encode(c) for c in s)[:3] for s in self.data['Suffix 2']]
        self.data['ASCII 2'] = ["".join("%d" % encode(c) for c in s)[3:] for s in self.data['Suffix 2']]

    def get_data_frame(self):
        return self.data
