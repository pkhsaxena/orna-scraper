import requests
import time
import json
import os
from bs4 import BeautifulSoup


def fetch_and_parse(url) -> bool:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = "".join(line.strip() for line in response.text.split('\n'))
        return parse(content)
    else:
        raise Exception(f'Failed to retrieve the webpage. Status code: {response.status_code}')


def parse(content) -> bool:
    soup = BeautifulSoup(content, 'html.parser')

    # can also do { "class": "codex-entries-entry" }
    bosses = soup.find_all('a', class_='codex-entries-entry')

    for boss in bosses:
        details = {}
        details['name'] = boss.contents[1].contents[0]
        details['family'] = boss.contents[2].contents[0]
        details['tier'] = boss.contents[3].contents[0].replace('\u2605', '')
        details['img'] = boss.contents[0].contents[0]['src']
        tag = {}
        tag[boss['href'].split("/")[-2]] = details
        json_data = json.dumps(tag)
        with open('temp.dump', 'a', encoding='utf-8') as codex:
            codex.write(json_data)
            codex.write('\n')

    pagination = soup.find('div', class_='pagination')
    return pagination is not None and "Next" in pagination.text


if __name__ == "__main__":
    page = 1
    url = f'https://playorna.com/codex/bosses/?p={page}'
    print(f'Requesting page {page}')
    while (fetch_and_parse(url)):
        time.sleep(10)
        page += 1
        print(f"Requesting page {page}")
        url = f'https://playorna.com/codex/bosses/?p={page}'

    codex_classes = []
    with open('temp.dump', 'r', encoding='utf-8') as content, open('bosses.json', 'w', encoding='utf-8') as codex:
        [codex_classes.append(json.loads(line)) for line in content]
        codex.write(json.dumps(codex_classes, indent=4))
    os.remove('temp.dump')
