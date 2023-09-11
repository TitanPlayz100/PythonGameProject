import json; from fuzzywuzzy import fuzz
with open('quotes.json', 'r') as file1:
    jsonData = json.loads(file1.read())
with open('raw_text_quotes.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(["("+i["author"]["name"]+"): "+i["content"] for i in jsonData["messages"] if ("\"" in i["content"]) or (("-" in i["content"]))]))

quotes_per_person = {"Unknown":[]}

for i in jsonData["messages"]:
    newMessage = i["content"].replace("\"", "").replace("\n", " \\\\").replace("|", "").split("-")
    person = newMessage[-1].replace(",", "").replace("|", "").replace("2021", "").replace("_", "").replace("2022", "").replace("2023", "").replace("Mr", "").replace("Ms", "").replace(".", "").strip() # Filter for grouping mentions of people better
    quote = "-".join(newMessage[0:-2]) if len(newMessage) > 2 else newMessage[0]
    quote = quote + " " + " ".join([j["url"] for j in i["attachments"]]) if " ".join([j["url"] for j in i["attachments"]]) != "" else quote
    if (len(newMessage) > 1) and (("\"" in i["content"]) or (("-" in i["content"]))):
            quotes = []
            for name in quotes_per_person:
                if fuzz.ratio(person.lower(), name.lower()) > 80: # Cool algorithm to better group people
                    quotes = quotes_per_person[name]
                    person = name
                    
            
            if quote != "": 
                quotes.append(quote)
                quotes_per_person[person] = quotes
    elif (("\"" in i["content"]) or (("-" in i["content"]))): 
            quotes_per_person["Unknown"].append(quote) if quote != "" else None

with open('quotes_per_mention.txt', 'w', encoding="utf-8") as f:
    f.write("\n".join(["<====== "+name+" "+str(len(quotes_per_person[name]))+" ======>\n"+"\n".join(quotes_per_person[name])+"\n<============>\n\n" for name in sorted(quotes_per_person, key=lambda name: len(quotes_per_person[name]), reverse=True)]) + "\nUsed the Levenshtein algorithm to try group names, as well as splitting at a '-'\nBadly formatted quotes found in 'Unknown'\nLinks of a message are under the quote")