# tools/url_content_tool.py
import requests

def url_content_tool(url):
    print("action: url_content_tool")
    print(f"Retrieving content from {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if response status is not successful
        content = response.text
        print(content)
        return content
    except requests.exceptions.RequestException as e:
        return f"Error retrieving content: {e}"
