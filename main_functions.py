import requests
from bs4 import BeautifulSoup
import os

COMMON_SUFFIXES = ['s', 'ly', 'es', 'ness', 'y', 'ing', 'tion', 'er', 'ism', 'ment', 'ant', 'ion', 'age',
                   'ship', 'ery', 'ic', 'd']
COMMON_WORDS = ['bake', 'word', 'list', 'four', 'five', 'nine', 'good', 'best', 'cute', 'zero', 'huge', 'cool',
                'tree', 'race', 'rice', 'keep', 'lace', 'beam', 'game', 'mars', 'tide', 'ride', 'hide', 'exit',
                'hope', 'cold', 'from', 'need', 'stay', 'come', 'also', 'able', 'acid', 'aged', 'away', 'baby',
                'back', 'bank', 'been', 'ball', 'base', 'busy', 'bend', 'bell', 'bird', 'came', 'calm', 'card',
                'coat', 'city', 'chat', 'cash', 'crow', 'cook', 'dark', 'each', 'evil', 'even', 'ever', 'face',
                'fact', 'fair', 'feel', 'fell', 'fire', 'fine', 'fish', 'gone', 'gold', 'girl', 'have', 'hair',
                'here', 'hear', 'into', 'iron', 'jump', 'kick', 'kill', 'life', 'like', 'love', 'main', 'move',
                'meet', 'more', 'nose', 'near', 'open', 'only', 'push', 'pull', 'sell', 'sale', 'that', 'this',
                'what', 'when', 'they', 'then', 'your', 'them', 'will', 'were', 'rank', 'with', 'time', 'make',
                'some', 'said', 'look', 'many', 'long', 'than', 'find', 'made', 'want', 'well', 'text', 'talk',
                'take', 'soft', 'rest', 'milk', 'hour', 'home', 'hold', 'give', 'down', 'note', 'yes', 'young',
                'about', 'above', 'after', 'again', 'against', 'always', 'another', 'answer', 'around', 'ask',
                'before', 'between', 'bring', 'building', 'call', 'can', 'case', 'cause', 'change', 'children',
                'close', 'color', 'country', 'course', 'day', 'different', 'door', 'during', 'early', 'earth',
                'end', 'family', 'father', 'feel', 'few', 'first', 'follow', 'food', 'friend', 'front', 'full',
                'group', 'grow', 'half', 'hand', 'happy', 'head', 'help', 'high', 'house', 'idea', 'important',
                'interest', 'large', 'learn', 'leave', 'letter', 'light', 'line', 'little', 'live', 'long',
                'lot', 'low', 'man', 'mean', 'mother', 'much', 'name', 'near', 'never', 'next', 'night', 'send',
                'number', 'off', 'often', 'page', 'part', 'place', 'play', 'point', 'power', 'public', 'seem',
                'question', 'quick', 'read', 'real', 'reason', 'right', 'run', 'same', 'school', 'second',
                'serve', 'set', 'show', 'small', 'sound', 'start', 'still', 'study', 'such', 'system', 'talk',
                'tell', 'thank', 'think', 'three', 'through', 'together', 'try', 'turn', 'under', 'understand',
                'until', 'use', 'voice', 'walk', 'watch', 'water', 'while', 'white', 'whole', 'word', 'work',
                'world', 'write', 'year']


def search_form_reversedictionary(base_word):
    url = f"https://reversedictionary.org/wordsfor/{base_word}"
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="html.parser")
    value = eval(soup.find("script", id="preloadedDataEl").contents[0])
    all_terms = value['terms']

    return all_terms


def search_from_relatedwords_io(base_word):
    final_lst = []
    url = f"https://relatedwords.io/{base_word}"
    html_doc = requests.get(url).content
    soup = BeautifulSoup(html_doc, features="html.parser")
    all_a_tags = soup.find_all(rel="nofollow")
    for word in all_a_tags:
        final_lst.append(word.get_text())

    return final_lst


def get_text_files(folder_name):
    base_files = os.listdir(folder_name)

    files = []
    for i in base_files:
        files.append(f"{folder_name}/{i}")

    return files


def text_file_combiner(folder_name="output"):
    text_files = get_text_files(folder_name)

    all_lines = []
    for file in text_files:
        with open(f"{file}", "r") as inp:
            words = inp.readlines()
        for word in words:
            the_word = word.replace("\n", "")
            if the_word not in all_lines:
                all_lines.append(the_word)

    final_lines = remove_common_words(all_lines)

    with open("final_list.txt", "w") as output:
        for i, word in enumerate(final_lines):
            if i == len(final_lines) - 1:
                output.write(word)  # Write the word without adding '\n'
            else:
                output.write(f"{word}\n")  # Add '\n' for all lines except the last one
    return text_files


def remove_common_words(lst):
    cleaned_list = []
    for word in lst:
        # Check if the word ends with any common suffix or is in the list of common words
        ends_with_common_suffix = any(word.endswith(suffix) for suffix in COMMON_SUFFIXES)
        is_common_word = word in COMMON_WORDS

        # If the word does not end with a common suffix and is not a common word, add it to cleaned_list
        if not ends_with_common_suffix and not is_common_word:
            cleaned_list.append(word)

    return cleaned_list

    # ONE LINE CODE:
    # return [word for word in lst if
    #         not any(word.endswith(suffix) for suffix in COMMON_SUFFIXES) and word not in COMMON_WORDS]


if __name__ == '__main__':
    pass

