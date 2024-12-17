import pandas as pd

class sa:
    def __init__(self):
        self.dict = pd.read_csv('Estimated_semantic_dimensions_word2vec_English.csv',)
        
    def to_v(self, data):
        motion_list = []
        d = self.dict.set_index('word')
        for w in data:
            w = w.lower()
            try:
                l = d.loc[w].tolist()
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