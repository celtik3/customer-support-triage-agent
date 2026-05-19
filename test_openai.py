from core.llm import llm

response = llm.invoke("Say hello in one short sentence.")

print(response.content)