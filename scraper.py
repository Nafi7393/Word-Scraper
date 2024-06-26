import random
from time import sleep
from random import randint
from main_functions import *


class WordScraper:
    def __init__(self, base_word, engine="reverse_dictionary"):
        self.already = []
        self.base = base_word
        self.all_final_words = None
        self.engine = engine

    def main_word_find(self):
        sleep(randint(3, 8))
        try:
            self.all_final_words = remove_common_words(self.search_for_words())
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to collect data for {self.base}: {e}")

    def search_for_words(self):
        if self.engine == "reverse_dictionary":
            all_terms = search_form_reversedictionary(self.base)
        elif self.engine == "related_words_io":
            final_lst = search_from_relatedwords_io(self.base)
            return final_lst
        else:
            raise ValueError("Invalid engine specified!")

        final_lst = [word["word"] for word in all_terms if self.possible(word["word"])]
        return final_lst

    def possible(self, word):
        if len(word) > 14 or len(word) <= 3:
            return False

        for letter in word:
            if not (97 <= ord(letter) <= 122) and letter != " ":
                return False

        if word in self.already or word in COMMON_WORDS:
            return False

        return True

    def output_this(self):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        with open(f"{output_dir}/{self.base}_{self.engine}.txt", "w") as output:
            for idx, word in enumerate(self.all_final_words):
                word = word.replace("-", "").lower()
                if idx < len(self.all_final_words) - 1:
                    output.write(f"{word}\n")
                else:
                    output.write(f"{word}")

        return True


if __name__ == '__main__':
    scraper = WordScraper(base_word="example word", engine=random.choice(["reverse_dictionary", "related_words_io"]))
    scraper.main_word_find()
    scraper.output_this()
