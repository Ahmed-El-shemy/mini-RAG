from app.helpers.config import get_settings ,Settings
import os

 
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.files_dir = os.path.join(self.base_dir, "assets/files")
    
    def generate_random_string(self, length: int = 16) -> str:
        """Generate a random string for unique file naming"""
        import string
        import random
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))