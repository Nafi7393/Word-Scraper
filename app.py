import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox
from scraper import WordScraper
from main_functions import text_file_combiner


class WordScraperGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.base_word_label = None
        self.base_word_input = None
        self.engine_label = None
        self.engine_input = None
        self.output_display = None
        self.scrape_button = None
        self.combine_button = None

        self.pos_x = 500
        self.pos_y = 300
        self.screen_width = 350
        self.screen_height = 400

        self.setWindowTitle('Word Scraper GUI')
        self.setGeometry(self.pos_x, self.pos_y, self.screen_width, self.screen_height)

        self.initUI()

    def initUI(self):
        self.base_word_label = QLabel('Base Word:')
        self.base_word_input = QLineEdit()

        self.engine_label = QLabel('Engine:')
        self.engine_input = QComboBox()  # Change to QComboBox for dropdown
        self.engine_input.addItem('reverse_dictionary')
        self.engine_input.addItem('related_words_io')
        self.engine_input.setCurrentIndex(0)  # Set default index

        # Output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        # Button to initiate scraping
        self.scrape_button = QPushButton('Scrape Words')
        self.scrape_button.clicked.connect(self.scrape_and_display)

        # Button to combine text files
        self.combine_button = QPushButton('Combine All Text Files From OUTPUT Folder')
        self.combine_button.clicked.connect(self.combine_text_files)
        self.combine_button.setStyleSheet("background-color: #4CAF50; color: white;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.base_word_label)
        layout.addWidget(self.base_word_input)
        layout.addWidget(self.engine_label)
        layout.addWidget(self.engine_input)
        layout.addWidget(self.scrape_button)
        layout.addWidget(self.output_display)
        layout.addWidget(self.combine_button)

        self.setLayout(layout)

    def scrape_and_display(self):
        base_word = self.base_word_input.text().strip()
        engine = self.engine_input.currentText().strip()

        if not base_word or not engine:
            self.output_display.clear()
            self.output_display.append('Please enter a base word and engine.')
            return

        try:
            scraper = WordScraper(base_word, engine)
            scraper.main_word_find()
            all_final_words = scraper.all_final_words
            scraper.output_this()

            self.output_display.clear()
            for idx, word in enumerate(all_final_words):
                self.output_display.append(f'{idx + 1}. {word}')

        except ValueError as ve:
            self.output_display.clear()
            self.output_display.append(str(ve))

        except RuntimeError as re:
            self.output_display.clear()
            self.output_display.append(str(re))

    def combine_text_files(self):
        try:
            all_files_locations = text_file_combiner(folder_name="output")
            self.output_display.clear()

            text = ""
            num = 1
            for i in all_files_locations:
                text += f"{num}.  {i}\n"
                num += 1
            text += f"\nAll the {len(all_files_locations)} Text Files combined successfully."

            self.output_display.append(text)

        except Exception as e:
            self.output_display.clear()
            self.output_display.append(f'Error combining text files: {str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WordScraperGUI()
    gui.show()
    sys.exit(app.exec_())
