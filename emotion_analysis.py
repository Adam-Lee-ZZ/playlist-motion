import time
import sys

class sa:
    def __init__(self, positive_dict, negative_dict):
        self.positive_dict = self.load_positive_dict(positive_dict)
        self.negative_dict = self.load_negative_dict(negative_dict)

 
    def load_positive_dict(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            word_dict = {}
            for items in lines:
                word_dict[items]=1
        return word_dict
    
    def load_negative_dict(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            word_dict = {}
            for items in lines:
                word_dict[items]=1
        return word_dict
    
    '''
    You can load more dict if you want. in Chinese, some of the well-known 
    dicts are 台灣大學NTUSD情感辭典; 清華大學開放中文詞庫; 大連理工大學中文情感詞彙本體庫;
    知網Hownet情感辭典. As for English, we have Verbnet, The Oxford English Dictionary 
    (OED) Semantic Domain for Motion, MOVES (Motion Verbs Semantics Database).
    each of them owns its features. you may take a overview before using.
    '''
    

    def findword(self, data):
        Pword_list = []
        Nword_list = []
        lines = data.split('\n')
        for line in lines:
            for items in line.strip().split(" "):

                if items in self.positive_dict:
                    Pword_list.append(items)
                elif items in self.negative_dict:
                    Nword_list.append(items)
        
        return len(Pword_list), len(Nword_list)
    
    '''
    As the scale of the data inceases, if * in *' may take a long time.
    to solve this, we can load dict as dict (using hash table to ensure 
    the selection costs less time).
    Instead of returing only the frecuency, you can use the weighted motion
    dict so that your returning will be a weighted score.
    the results can be used both in machine learning and straightly in 
    data visualisation.
    '''

def score(po,ne,data):
    dict = sa(po,ne)
    result = sa.findword(dict,data)
    return result
