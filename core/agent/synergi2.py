import g4f 

provider = g4f.Provider.Aichat

# Streaming is not supported by these providers
if provider in {g4f.Provider.Aws, g4f.Provider.Ora,
                g4f.Provider.Bard, g4f.Provider.Aichat}:
    stream = False
else:
    stream = True

print(provider.params)  # supported args

class SynergiAgent:
    def __init__(self):
        pass

    def handle_message(self, message):
        print(message)
        message_text = message.get('sendMessage', '') 
        response = g4f.ChatCompletion.create(model='gpt-4',
                                             messages=[{"role": "user",
                                                        "content": message_text}],
                                             stream=stream,
                                             provider=provider)

        print(response)
        return response
