import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.text_splitter import extract_docs

docs = extract_docs('example/9787115592316.epub')

print(docs)