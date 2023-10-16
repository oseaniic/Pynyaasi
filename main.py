import fetch

lest = fetch.scrap('https://nyaa.si/?f=0&c=2_0&q=')

for i in lest:
    print()
    print(i)