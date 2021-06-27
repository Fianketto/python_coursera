from bs4 import BeautifulSoup
import re
import os
import unittest


def parse(path_to_file):
    h_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    with open(path_to_file, 'r', encoding='utf-8') as fin:
        file_content = fin.read()
        soup = BeautifulSoup(file_content, 'lxml')
    body_content = soup.find('div', id="bodyContent")

    # 1. img
    img_list = [img for img in body_content.find_all('img') if int(img.get('width', 0)) >= 200]
    imgs = len(img_list)

    # 2. header
    header_list = [h for h in body_content.find_all(h_list) if re.match(r"^[ETC]", h.text)]
    headers = len(header_list)

    # 3. link
    link_list = body_content.find_all('a')
    in_a_row_count = [1 for i in range(len(link_list))]
    for i in range(len(link_list)):
        current_in_a_row = 1
        link = link_list[i]
        next_sibling = link.find_next_siblings()
        for sibling in next_sibling:
            if sibling.name == 'a':
                current_in_a_row += 1
            else:
                break
        in_a_row_count[i] = current_in_a_row
    linkslen = max(in_a_row_count)

    # 4. ul, ol
    ul_list = body_content.find_all(['ul', 'ol'])
    ul_count = 0
    for ul in ul_list:
        parents = ul.find_parents()
        is_nested = False
        for p in parents:
            if p.name in ['ul', 'ol']:
                is_nested = True
                break
        if not is_nested:
            ul_count += 1

    lists = ul_count

    return [imgs, headers, linkslen, lists]


def get_all_links(path, page):
    try:
        with open(os.path.join(path, page), encoding="utf-8") as file:
            links = set(re.findall(r"(?<=/wiki/)[\w()]+", file.read()))
    except FileNotFoundError:
        links = set()
    return links


def build_bridge(path, start_page, end_page):
    if start_page == end_page:
        return [start_page]
    edges = {}
    parents = {}
    links = get_all_links(path, start_page)

    edges[start_page] = links
    parents[start_page] = None
    used = {start_page}

    path_found = False
    queue = [start_page]

    while not path_found and queue:
        current_page = queue.pop(0)
        temp_queue_set = set(queue)

        links = get_all_links(path, current_page)
        new_links = [link for link in links if link not in temp_queue_set and link not in used]

        queue.extend(new_links)
        for link in new_links:
            parents[link] = current_page
            used.add(link)

        for link in new_links:
            if link == end_page:
                path_found = True
                break

    steps = [end_page]
    parent = parents[end_page]

    if path_found:
        while parent:
            steps.append(parent)
            parent = parents[parent]

    steps.reverse()
    return steps


def get_statistics(path, start_page, end_page):
    pages = build_bridge(path, start_page, end_page)
    statistic = {}
    for page in pages:
        stat = parse(os.path.join(path, page))
        statistic[page] = stat
    return statistic


'''
class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)
'''


if __name__ == '__main__':
    #unittest.main()
    path_to_file = 'wiki/Stone_Age'
    parse(path_to_file)
    result = get_statistics('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing")
    print(result)
