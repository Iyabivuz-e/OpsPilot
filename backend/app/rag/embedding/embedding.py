from sentence_transformers import SentenceTransformer
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class Embedding:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    
    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=20), # retry after 2 seconds, if too much dont exceed 20 secs
        retry=retry_if_exception_type(Exception)
    )
    def embed(self, text) -> list[float]:
        try:
            return self.model.encode(text).tolist()
        except Exception as e:
            # Will put logging later
            print(f"Failed to generate embeddings for batch: {e}")
            raise e
        

class EmbeddingBacher:
    def __init__(self, batch_size: int = 64 ):
        self.batch_size = batch_size
        
    def get_batches(self, chunks):
        for i in range(0, len(chunks), self.batch_size):
            yield chunks[i:i + self.batch_size]