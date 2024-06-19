import os
from time import sleep
from random import randint
import requests
from bs4 import BeautifulSoup


def remove_common_words(lst):
    for word in lst:
        check_words = [word + "s", word + "ly", word + "es", word + "ness", word + "y", word + "ing", word + "tion",
                       word + "er", word + "ism", word + "ment", word + "ant", word + "ion", word + "age",
                       word + "ship", word + "ery", word + "ic", word + "d"]

        if word in check_words:
            try: lst.remove(word)
            except: pass

    return lst


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

    with open(f"Final_Combined.txt", "w") as output:
        for word in final_lines:
            output.write(f"{word}\n")


class WordScraper:
    def __init__(self, base_word):
        self.already = []
        self.base = base_word
        self.all_final_words = None
        self.main_word_find()
        self.output_this()

    def main_word_find(self):
        sleep(randint(3, 8))
        try:
            self.all_final_words = remove_common_words(self.search_for_words())
        except Exception:
            raise f"Failed to collect data for {self.base}"

    def search_for_words(self):
        final_lst = []
        url = f"https://reversedictionary.org/wordsfor/{self.base}"
        html_doc = requests.get(url).content
        soup = BeautifulSoup(html_doc, features="html.parser")
        value = eval(soup.find("script", id="preloadedDataEl").contents[0])
        all_terms = value['terms']
        for get in all_terms:
            word = get["word"]
            if self.possible(word):
                self.already.append(word)
                final_lst.append(word)

        return final_lst

    def possible(self, word):
        if len(word) > 14 or len(word) <= 3:
            return False

        for letter in word:
            if ord(letter) in range(97, 123):
                pass
            elif letter == " ":
                pass
            else:
                return False
        if word in self.already:
            return False

        common_words = ['bake', 'word', 'list', 'four', 'five', 'nine', 'good', 'best', 'cute', 'zero', 'huge', 'cool',
                        'tree', 'race', 'rice', 'keep', 'lace', 'beam', 'game', 'mars', 'tide', 'ride', 'hide', 'exit',
                        'hope', 'cold', 'from', 'need', 'stay', 'come', 'also', 'able', 'acid', 'aged', 'away', 'baby',
                        'back', 'bank', 'been', 'ball', 'base', 'busy', 'bend', 'bell', 'bird', 'came', 'calm', 'card',
                        'coat', 'city', 'chat', 'cash', 'crow', 'cook', 'dark', 'each', 'evil', 'even', 'ever', 'face',
                        'fact', 'fair', 'feel', 'fell', 'fire', 'fine', 'fish', 'gone', 'gold', 'girl', 'have', 'hair',
                        'here', 'hear', 'into', 'iron', 'jump', 'kick', 'kill', 'life', 'like', 'love', 'main', 'move',
                        'meet', 'more', 'nose', 'near', 'open', 'only', 'push', 'pull', 'sell', 'sale', 'that', 'this',
                        'what', 'when', 'they', 'then', 'your', 'them', 'will', 'were', 'rank', 'with', 'time', 'make',
                        'some', 'said', 'look', 'many', 'long', 'than', 'find', 'made', 'want', 'well', 'text', 'talk',
                        'take', 'soft', 'rest', 'milk', 'hour', 'home', 'hold', 'give', 'down', 'note']

        if word in common_words:
            return False

        return True

    def output_this(self):
        with open(f"output/{self.base}.txt", "w") as output:
            for word in self.all_final_words:
                word.replace("-", "")
                word = word.lower()
                output.write(f"{word}\n")
        return True


if __name__ == '__main__':
    text_file_combiner()
