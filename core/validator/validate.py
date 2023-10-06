from llms.llms import Model  
class  retroactive_validator:
     def __init__(self,master_prompt):
         self.master_prompt=master_prompt
     def validate(self,result):
            def extract_json(text):
               print("the init")
               print(text)
               start_index = text.index('{')
               end_index = text.rindex('}') + 1
               # Extract the JSON substring
               json_string = text[start_index:end_index]
               # Parse the JSON string into a Python dictionary
               try:
                  json_obj = json.loads(json_string)
                  return json_obj
               except json.JSONDecodeError:
                  print("oops no json!")
            prompt="""You are a validator agent your mission is to validate the data a LLMS(Large Language Models) model are return in a precedent request the prompt of the request to the NLP Prompt:{prompt}
            the text I give the NLP:{text} the response of the LLMS:{response}
            return a JSON with this field"""
            prompt=prompt.format(prompt=self.master_prompt,text=result.text,response=result.response)
            prompt +="""
            {
               is_valid:Boolean if the response of NLP is Valid,
               type_of_response:if not valid give the type of reponse attended JSON,string,numbe....,
               corrector_prompt:a sentence to correct the reponse in the recursive action 
            }
            """
            model = Model("gpt3", master_prompt=prompt, api_key="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")
            response=model.generate_text('the json you return:')
            response=extract_json(response)
            if(response['is_valid']):
                  return result.response
            else:
               print("The response is not valid activate retroaction!!!")
               return self.corrector(master_prompt,result.response,response['corrector_prompt'],response['type_of_response'])
     def corrector(prompt,old_response,corrector_prompt,type_of_response):
          model = Model("gpt3", master_prompt=prompt, api_key="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")
          text_given="""
              your old response:{old_response}\n
              how to correct them:{corrector_prompt}\n
              the type of response attended:{type_of_response}
              the correct response:
          """
          text_given=text_given.format(old_response=old_response,corrector_prompt=corrector_prompt,type_of_response=type_of_response)
          response=model.generate_text(text_given)
          response=self.validate({
            'text':text_given,
            'response':response
          })
          return response
      
     