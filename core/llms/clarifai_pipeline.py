from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

class ClarifaiAPI:
    def __init__(self,model_name):
        #condition to detect the name of the model 
        if model_name.lower() == 'gpt3':
           self.USER_ID = 'openai'
           self.APP_ID = 'chat-completion'
           self.MODEL_ID = 'GPT-3_5-turbo'
           self.MODEL_VERSION_ID = '8ea3880d08a74dc0b39500b99dfaa376'
        elif model_name.lower() == 'gpt4':
             self.USER_ID = 'openai'
             self.APP_ID = 'chat-completion'
             self.MODEL_ID = 'GPT-4'
             self.MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'
        elif model_name.lower() == 'claudev2':
             self.USER_ID = 'anthropic'
             self.APP_ID = 'completion'
             self.MODEL_ID = 'claude-v2'
             self.MODEL_VERSION_ID = 'cd8f314bf81f4c24b006af002e827122'
        elif model_name.lower()=='claudev1.2':
            self.USER_ID = 'anthropic'
            self.APP_ID = 'completion'
            self.MODEL_ID = 'claude-instant-1_2'
            self.MODEL_VERSION_ID = '710652a9f5c0439086c4dd96170c596a'
        elif model_name.lower() == 'jurassic':
             self.USER_ID = 'ai21'
             self.APP_ID = 'complete'
             self.MODEL_ID = 'Jurassic2-Large'
             self.MODEL_VERSION_ID = '4ccdadffa2d24af288c1d4b8410a7027'
        elif model_name.lower() == 'stable-diffusion-xl-beta':
             self.USER_ID = 'stability-ai'
             self.APP_ID = 'stable-diffusion-2'
             self.MODEL_ID = 'stable-diffusion-xl-beta'
             self.MODEL_VERSION_ID = '1c7531ddae654dd58de8a8e93271484e'
        elif model_name.lower() == 'stable-diffusion-xl':
             self.USER_ID = 'stability-ai'
             self.APP_ID = 'stable-diffusion-2'
             self.MODEL_ID = 'stable-diffusion-xl'
             self.MODEL_VERSION_ID = '0c919cc1edfc455dbc96207753f178d7'
        elif model_name.lower() == "embedada":
             self.USER_ID = 'openai'
             self.APP_ID = 'embed'
             self.MODEL_ID = 'text-embedding-ada'
             self.MODEL_VERSION_ID = '7a55116e5fde47baa02ee5741039b149'
        elif model_name.lower() == 'blip2':
            self.USER_ID = 'salesforce'
            self.APP_ID = 'blip'
            self.MODEL_ID = 'general-english-image-caption-blip-2'
            self.MODEL_VERSION_ID = '71cb98f572694e28a99fa8fa86aaa825'
        else:
            raise ValueError(f"Invalid model name: {model_name}")
        self.PAT = 'f241078d1c8d404498b31cfe62f1df70'
        self.channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(self.channel)
        self.metadata = (('authorization', 'Key ' + self.PAT),)
        self.userDataObject = resources_pb2.UserAppIDSet(user_id=self.USER_ID, app_id=self.APP_ID)

    def predict_concepts(self, text_file_url):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                url=text_file_url
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        return output
    def predict_images(self, image_file_url):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                url=image_file_url
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
        print(post_model_outputs_response)
        output = post_model_outputs_response.outputs[0]
        print(output)
        print(f"Text captionning:{output['data']['text']['raw']}")
        return output
    def predict_video(self, video_file_url):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            video=resources_pb2.Video(
                                url=video_file_url
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        return output
    #predict image with bytes 
    def predict_images_bytes(self,bytes):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                base64=bytes
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        return output
    #predict video with bytes
    def predict_video_bytes(self,bytes):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            video=resources_pb2.Video(
                                base64=bytes
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        return output
    #predict concepts with bytes
    def predict_text_raw(self,raw):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=raw
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        print(output)
        return output
    #predict concepts with bytes
    def generate_image_with_text(self,raw):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=raw
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        print(output)
        return output
    def generate_text_embedding(self,raw):
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=raw
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        output = post_model_outputs_response.outputs[0]
        
        print(f"Text embedding:{output.data.embeddings[0].vector}")
        #return output['data']['embeddings'][0]['vector']

