import os
import re


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


steps = build_bridge('wiki/', 'The_New_York_Times', 'Stone_Age')

