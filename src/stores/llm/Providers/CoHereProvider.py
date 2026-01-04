from ..LLMInterface import LLMInterface
from ...LLMEnums import CoHereEnums
from ...LLMEnums import DocumentEnums
import cohere
import logging

class CoHereProvider(LLMInterface):
    def __init__(self,
                 api_key:str,
                 api_url:str,
                 default_inpot_max_characters:int=1000,
                 default_generation_max_output_tokens:int=1000,
                 default_generation_temperature:float=0.1):
                 
    
        self.api_key = api_key

        self.default_inpot_max_characters = default_inpot_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model = None

        self.embeddings_model_id = None
        self.embeddings_size = None

        self.client = cohere.Client(api_key=api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self,model_id:str):
        self.generation_model = model_id


    def set_embeddings_model( self , model_id : str , embedding_size:int):
        self.embeddings_model_id = model_id
        self.embeddings_size = embedding_size

    def process_txt(self , text:str):
        return text[:self.default_inpot_max_characters].strip()

    def generate_text( self , model_id : str , chat_history :list[],max_output_tokens:int
                           temperature:float =None):
        
        if not self.client:
            self.logger.error("CoHere client is not set")
            return None

        if not self.generation_model:
            self.logger.error("Generation model is not set")
            return None 

        response = self.client.chat(
            model = self.generation_model,
            chat_history = chat_history,
            message = self.process_txt(prompt),
            max_tokens = max_output_tokens,
            
            
        )

        if not response or not response.text :
            self.logger.error("Error while generating text with CoHere")
            return None


    def embed_text(self,text : str , document_type:str =None):
        if not self.client:
            self.logger.error("Error while generating embeddings with CoHere")
            return None

        if not self.embeddings_model_id:
            self.logger.error("Embeddings model is not set")
            return None
        
        input_type = CoHereEnums.DOCUMENT.value
        if document_type == DocumentEnums.QUERY:
            input_type = CoHereEnums.QUERY.value

         response = self.client.embed(
            model = self.embedding_model_id,
            texts = (self.process_txt(text)),
            input_type = input_type
            embedding_type =['float'] ,
         )

        if not response or not response.embeddings or not response.embeddings[0]:
            self.logger.error("Error while generating embeddings with CoHere")
            return None

        return response.embeddings.float[0]

    def construct_prompt(self, prompt:str, role:str):
        return {
            "role":role,
            "text":self.process_txt(prompt)
        }
