import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.llm import llm

response = llm.invoke("Say hello in one short sentence.")

print(response.content)