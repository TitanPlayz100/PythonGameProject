import json,requests,multiprocessing
if __name__=='__main__':
    with multiprocessing.Pool(8)as pool:
        with open('memes_chat.json','r',encoding="utf-8")as file1:
            for i in json.loads(file1.read())["messages"]:
                for j in i["embeds"]:
                    if"."in j["url"].split("/")[-1].split("?")[0]:
                        open(j["url"].split("/")[-1].split("?")[0],'wb').write(requests.get(j["url"],allow_redirects=True).content)       
                for j in i["attachments"]:
                    if"."in j["url"].split("/")[-1].split("?")[0]:
                        open(j["url"].split("/")[-1].split("?")[0],'wb').write(requests.get(j["url"],allow_redirects=True).content)