import json, requests; from multiprocessing.pool import ThreadPool
count = 0

def get_data(filename):
    with open(filename, 'r', encoding="utf-8") as file1:
        data: dict = json.loads(file1.read())
    return data

def get_links(data):
    a = []
    for i in data["messages"]:
        links = i["embeds"] + i["attachments"]
        for j in links:
            a.append(j["url"])
    return a

def download_url(url:str):
    global count
    r = requests.get(url, allow_redirects=True)
    name:str = url.split("/")[-1].split("?")[0]
    if "." in name:
        open(name, 'wb').write(r.content)
        count += 1
        print(f"{count}: Downloaded {name}")

if __name__ == '__main__':
    data = get_data('memes_chat.json')
    urls = get_links(data)
    ThreadPool(8).imap_unordered(download_url, urls)