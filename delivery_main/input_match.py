from konlpy.tag import Okt
import json
from gensim.models import fasttext

okt = Okt()

def preprocessing(input):
    tokens = okt.pos(input, norm=True, stem=True)
    result = []
    for t in tokens:
        if (t[1] in ['Noun', 'Adjective']): result.append(t)
    return result

with open('C:\\Users\\김주호\\Desktop\\delivery_service_re\\food_atr.json', 'r', encoding='utf-8') as atr_file:
   atr_list = json.load(atr_file)

model = fasttext.load_facebook_model('C:\\Users\\김주호\\Desktop\\delivery_service_re\\wiki.ko.bin')
def feature_match(tokens, atr_list):
   sim_list = []
   result = ''

   if (len(tokens) >= 1):
       for atr in atr_list:
           sim_list.append((atr, model.wv.similarity(tokens[0][0], atr)))
       result = max(sim_list, key=lambda x: x[1])[0]
   return result