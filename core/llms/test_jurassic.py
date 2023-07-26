from jurassic import Jurassic

def test_generate():
    jurassic = Jurassic(api_key='test_api_key')
    prompt = 'Hi'
    output = jurassic.generate(prompt)
    print(f"Output: {output}")

test_generate()