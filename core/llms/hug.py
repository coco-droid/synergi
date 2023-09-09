import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/git-base"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("teddy-bear.png")

print(output)









#import requests

#API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-1-pythia-12b"
#headers = {"Authorization": "Bearer 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"}

#def query(payload):
	# response = requests.post(API_URL, headers=headers, json=payload)
	#return response.json()
	
#output = query({
	#"inputs": "how are you doing today?",
#})

#print(output)

