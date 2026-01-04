from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI


class OpenAIProvider(LLMInterface):
    
    def __init__(self ,api_key: str, api_url:str=None ,
                    default_inpot_max_characters:int=1000,
                    default_generation_max_output_tokens:int=1000,
                    default_generation_temperature:float=0.1);
                
    
    self.api_key = api_key
    self.api_url = api_url

    self.default_inpot_max_characters = default_inpot_max_characters
    self.default_generation_max_output_tokens = default_generation_max_output_tokens
    self.default_generation_temperature = default_generation_temperature

    self.generation_model = None

    self.embeddings_model_id = None
    self.embeddings_size = None

    self.client = OpenAI(
        api_key=self.api_key,
        api_base=self.api_url
    )

    self.logger = logging.getLogger(__name__)
    
    def set_generation_model(self,model_id:str):
        self.generation_model = model_id

    def set_embeddings_model( self , model_id : str , embedding_size:int):
        self.embeddings_model_id = model_id
        self.embeddings_size = embedding_size


    def process_txt(self , text:str):
        return text[:self.default_inpot_max_characters].strip()
        

    def generate_text(self, prompt:str , chat_history :list[],max_output_tokens:int
                           temperature:float =None):
        
        if not self.client:
            self.logger.error("OpenAI client is not set")
            return None 
        
        if not self.generation_model:
            self.logger.error("Generation model for OpenAI is not set")
            return None 

        max_output_tokens = max_output_tokens if max_output_tokens  
        else self.default_generation_max_output_tokens

        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt , role = OpenAIEnums.USER.value)
        )

        response = self.client.chat.completions.create(
            model=self.generation_model,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].messages   
        self.logger.error("Error while generating text with OpenAI")
        return None 

        return response.choices[0].message.["content"]

        

    raise NotImplementedError

    def embed_text( self , text:str, document_type:str):

        if not self.client:
            self.logger.error("OpenAI client is not set")
            return None 
        
        if not self.embeddings_model_id:
            self.logger.error("Embeddings model is not set")
            return None 
        
        response = self.client.embeddings.create(
            model= self.embeddings_model_id,
            input=text
        )

        if not response:
            self.logger.error("Error while embedding text with OpenAI")
            return None
        
        return response.data[0].embedding

    def construct_prompt(self, prompt:str ,role:str):
        return {
            "role":role,
            "content":self.process_txt(prompt)
        }
        
        

