import json
import requests
from multiprocessing import Pool

count = 0

def get_data():
    with open('memes_chat.json', 'r', encoding="utf-8") as file1:
        jsonData = json.loads(file1.read())

    for i in jsonData["messages"]:
        embeds: list = i["embeds"]
        attachments: list = i["attachments"]
        for j in embeds:
            url = j["url"]
            download_url(url)        
        for j in attachments:
            url = j["url"]
            download_url(url)          

def download_url(url:str):
    global count
    r = requests.get(url, allow_redirects=True)
    name = url.split("/")[-1]
    name1 = name.split("?")[0]
    if "." in name1:
        open(name1, 'wb').write(r.content)
        count += 1
        print(f"{count}: Downloaded {name1}")

if __name__ == '__main__':
    with Pool(8) as pool:
        get_data()

