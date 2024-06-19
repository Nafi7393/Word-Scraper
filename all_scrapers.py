import requests
from bs4 import BeautifulSoup


def search_form_reversedictionary(base_word):
    url = f"https://reversedictionary.org/wordsfor/{base_word}"
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="lxml")
    value = eval(soup.find("script", id="preloadedDataEl").contents[0])
    all_terms = value['terms']
    extracted_word = []
    for get in all_terms:
        extracted_word.append(get["word"])

    return extracted_word


def search_from_relatedwords_io(base_word):
    final_lst = []
    url = f"https://relatedwords.io/{base_word}"
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="lxml")
    all_a_tags = soup.find_all(rel="nofollow")
    for word in all_a_tags:
        final_lst.append(word.get_text())

    return final_lst


def old_swear_1950():
    path = "1950s swear word.html"
    f = open(path, encoding="utf8")
    soup = BeautifulSoup(f, )
    f.close()

    final_lst = []

    target = soup.find_all(width="150")
    for word in target:
        get = word.get_text()
        if get:
            if "\n" not in get:
                final_lst.append(get)

    return final_lst


if __name__ == '__main__':
    pass
































