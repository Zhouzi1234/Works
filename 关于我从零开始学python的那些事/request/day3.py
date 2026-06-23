from day2 import clean_text
import json
with open('requests_file.json','r',encoding='utf-8') as f:
    book=json.load(f)##[{'title': 'Frankenstein', 'content':..
    ls=clean_text(book)
with open('requestsjson.json','w',encoding='utf-8') as b:
        json.dump(ls,b,ensure_ascii=False,indent=2)
'''EN_STOPWORDS = {"the", "and", "of", "in", "a", "is", "was", "were", "it", "i", "my"}
words = content.split()
content = ' '.join([w for w in words if w not in EN_STOPWORDS])'''