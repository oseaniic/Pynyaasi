import requests
from bs4 import BeautifulSoup

url = 'https://nyaa.si/?f=0&c=2_0&q='
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all anchor tags and extract their 'href' attributes
    links = [link.get('href') for link in soup.find_all('a')]
    
    # Print the extracted links
    for link in links:
        print(link)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
