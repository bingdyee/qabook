import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rag_chain import get_rag_response 


rs = get_rag_response("如何快速成稿？")

print(rs)