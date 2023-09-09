# tools/duckduckgo_tool.py
from duckduckgo_search import DDGS

ddgs = DDGS()

def duckduckgo_tool(query):
    print(query)
    results = []
    for r in ddgs.answers(query):
        #print(r)
        results.append(r)
    if results:
        #print(results)
        #return the first result url
        return results[0]['url']
    else:
        return "No images found."
