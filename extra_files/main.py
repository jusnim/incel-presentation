import requests
import json


class wiki_page:
    def __init__(self, name, links):
        self.name = name
        self.links = links


list_of_wiki_pages = []
set_of_all_tracked_links = set()


def main():
    ### make request to website and get results
    for id in range(0, 10000):
        if id % 100 == 0:
            print(id)
        response = requests.get(f"https://incel.wiki/index.php?curid={id}")
        name = response.text.split('wgPageName":"')[1].split('","')[0]
        if name == "Special:Badtitle":
            continue

        # get all links
        links = []
        for link in response.text.split('href="')[1:]:
            link = link.split('"')[0]
            if link.startswith("/"):
                links.append(link)

        # remove duplicates
        links = list(set(links))

        # remove links with #
        links = [link for link in links if "#" not in link]

        # filter all links which are not wiki pages
        links = [link for link in links if link.startswith("/w")]

        # remove /w from each link
        links = [link[3:] for link in links]

        for link in links:
            set_of_all_tracked_links.add(link)

        wiki_page_object = wiki_page(name, links)
        list_of_wiki_pages.append(wiki_page_object)

    # rerun_on_leftover_links()

    # save all links to a json file

    with open("links.json", "w") as f:
        json.dump([page.__dict__ for page in list_of_wiki_pages], f)


count = 0


def rerun_on_leftover_links():
    if count > 1:
        return
    global set_of_all_tracked_links
    print(set_of_all_tracked_links)
    for page in list_of_wiki_pages:
        if page.name in set_of_all_tracked_links:
            set_of_all_tracked_links.remove(page.name)

    if len(set_of_all_tracked_links) == 0:
        return

    tmp = set([])
    for link in set_of_all_tracked_links:
        response = requests.get(f"https://incel.wiki/w/{link}")
        name = response.text.split('wgPageName":"')[1].split('","')[0]
        if name == "Special:Badtitle":
            continue

        print("do")

        links = []
        for link in response.text.split('href="')[1:]:
            link = link.split('"')[0]
            if link.startswith("/"):
                links.append(link)

        # remove duplicates
        links = list(set(links))

        # remove links with #
        links = [link for link in links if "#" not in link]

        # filter all links which are not wiki pages
        links = [link for link in links if link.startswith("/w")]

        # remove /w from each link
        links = [link[3:] for link in links]

        for link in links:
            if link not in [page.name for page in list_of_wiki_pages]:
                tmp.add(link)

        wiki_page_object = wiki_page(name, links)
        list_of_wiki_pages.append(wiki_page_object)

    set_of_all_tracked_links = tmp
    rerun_on_leftover_links()


def preprocess_data():
    with open("links.json", "r") as f:
        list_of_wiki_pages = json.load(f)
        # print(list_of_wiki_pages[0]["name"])
        list_of_list_of_links = [page["links"] for page in list_of_wiki_pages[::]]

        # count each link
        link_count = {}
        for list_of_link in list_of_list_of_links:
            for link in list_of_link:
                if link in link_count:
                    link_count[link] += 1
                else:
                    link_count[link] = 1
        print(link_count)

        blacklist = [
            "Special:Random",
            "Special:Badtitle",
            "Special:RecentChanges",
            "Special:RandomInCategory/IncelWiki",
            "Special:SpecialPages",
            "Special:Categories",
            "Special:AllPages",
            "Incel_Wiki:About",
        ]

        # remove blacklisted links
        for link in blacklist:
            if link in link_count:
                link_count.pop(link)

        # remove all links with count 5195 (sidebar)
        tmp = link_count.copy()
        for link in link_count:
            if link_count[link] == 5195:
                tmp.pop(link)
        link_count = tmp

        # print top 10 links
        sorted_link_count = sorted(link_count.items(), key=lambda x: x[1], reverse=True)

        def getTab(stri):
            return f"\t" if len(str(stri)) > 3 else f"\t\t"

        with open("links.txt", "w") as f:
            for link in sorted_link_count:
                f.write(f"{link[1]}{getTab(link[1])}{link[0]}\n")


if __name__ == "__main__":
    preprocess_data()
    # main()
