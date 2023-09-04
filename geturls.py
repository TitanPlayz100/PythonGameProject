from pytube import Playlist


urls = []

playlisturl = Playlist("https://www.youtube.com/playlist?list=PLyUioSShhnYoVge1lWTEeueAbxFjQ1yvY")

for url in playlisturl:
    urls.append(url)

with open('playlist_urls.txt', 'w') as file:
    for url in urls:
        file.write(url+'\n')

duplicateurls = []
urls2 = []

for i in urls:
    if i not in urls2:
        urls2.append(i)
    else:
        duplicateurls.append(i)

with open('duplicate_urls.txt', 'w') as file:
    for url in duplicateurls:
        file.write(url+'\n')
