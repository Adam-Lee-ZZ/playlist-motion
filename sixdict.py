import pandas as pd
import os
os.environ['MPLCONFIGDIR'] = '/tmp'

class sa:
    def __init__(self):
        self.dict = pd.read_csv('static/dic/Estimated_semantic_dimensions_word2vec_English.csv',)
        
    def to_v(self, data):
        data = data.replace('\n',' ').split(' ')
        print(data)
        motion_list = []
        d = self.dict.set_index('word')
        for w in data:
            w = w.lower()
            print(w)
            try:
                l = d.loc[w].tolist()
                print(l)
                motion_list.append(l)
            except KeyError:
                continue

        motion = pd.DataFrame(motion_list)
        motion.columns = ['Vision','Motor','Socialness',
                          'Emotion','Emotion_abs+1','Time','Space']
        
        return motion

if __name__ == '__main__':
    s = sa()
    s.to_v(['a'])