import requests, time, json
from bs4 import BeautifulSoup

def fetch_and_save_html(url, file_name):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0'}    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

def parse(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        content = "".join(line.strip() for line in content.split('\n'))

    soup = BeautifulSoup(content, 'html.parser')

    # can also do { "class": "codex-entries-entry" }
    items = soup.find_all('a', class_='codex-entries-entry')

    for item in items:
        details = {}
        details['name']=item.contents[1].contents[0]
        details['tier'] = item.contents[2].contents[0].replace('\u2605','')
        details['rarity'] = item.contents[0].contents[0]['class'][0]
        details['img'] = item.contents[0].contents[0]['src']
        json_data = json.dumps(details)
        with open('temp.dump','a', encoding='utf-8') as codex:
            codex.write(json_data)
            codex.write('\n')

if __name__ == "__main__":
    for i in range(1,62):
        url = f'https://playorna.com/codex/items/?p={i}'
        print(f'Requesting page {i}')
        file_name = 'page.html'

        fetch_and_save_html(url, file_name)
        parse(file_name)
        time.sleep(10)

    codex_items=[]
    with open('temp.dump','r',encoding='utf-8') as content, open('codex.json', 'w', encoding='utf-8') as codex:
        [codex_items.append(json.loads(line)) for line in content]
        codex.write(json.dumps(codex_items,indent=4))
    
