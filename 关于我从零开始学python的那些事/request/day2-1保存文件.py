from day2 import main
import json
if __name__=="__main__":
    books=main()
    with open('requests_file.json','a+',encoding='utf-8') as file:
        json.dump(books,file,ensure_ascii=False,indent=2)
