import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from example.reader import BookReader


def run_example():
    book_path = 'example/9787115592316.epub'
    reader = BookReader('deepseek-r1:14b')
    reader.learn(file_path=book_path)
    print(reader.query("What is the title of the book?"))


run_example()