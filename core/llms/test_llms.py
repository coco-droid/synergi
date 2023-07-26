from llms import Model

def test_gpt3():
    model = Model('gpt3')
    user_input = "What is the meaning of life?"
    response = model.generate_text(user_input)
    assert isinstance(response, str)
    assert len(response) > 0
    print(response)

test_gpt3()