"""
PhotoRoom API client for AI-powered image editing
"""
import requests
import io
from typing import Optional, Dict, Any
from PIL import Image
from config import PHOTOROOM_API_KEY, PHOTOROOM_BASE_URL


class PhotoRoomClient:
    def __init__(self):
        self.api_key = PHOTOROOM_API_KEY
        self.base_url = PHOTOROOM_BASE_URL
        
        if not self.api_key:
            raise ValueError("PhotoRoom API key must be provided")
    
    def _make_request(self, endpoint: str, files: Dict = None, data: Dict = None) -> requests.Response:
        """Make a request to the PhotoRoom API"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'X-Api-Key': self.api_key
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"PhotoRoom API request failed: {str(e)}")
    
    def remove_background(self, image_data: bytes, format: str = "PNG") -> bytes:
        """Remove background from an image"""
        files = {
            'image_file': ('image.jpg', image_data, 'image/jpeg')
        }
        data = {
            'format': format
        }
        
        try:
            response = self._make_request('segment', files=files, data=data)
            return response.content
        except Exception as e:
            raise Exception(f"Failed to remove background: {str(e)}")
    
    def change_background(self, image_data: bytes, background_prompt: str = "white background", format: str = "PNG") -> bytes:
        """Change the background of an image using AI"""
        files = {
            'image_file': ('image.jpg', image_data, 'image/jpeg')
        }
        data = {
            'background_prompt': background_prompt,
            'format': format
        }
        
        try:
            # Use the instant-backgrounds endpoint for background replacement
            response = self._make_request('instant-backgrounds', files=files, data=data)
            return response.content
        except Exception as e:
            raise Exception(f"Failed to change background: {str(e)}")
    
    def enhance_image(self, image_data: bytes, format: str = "PNG") -> bytes:
        """Enhance image quality using PhotoRoom's AI"""
        files = {
            'image_file': ('image.jpg', image_data, 'image/jpeg')
        }
        data = {
            'format': format
        }
        
        try:
            # Use segment endpoint with enhancement
            response = self._make_request('segment', files=files, data=data)
            return response.content
        except Exception as e:
            raise Exception(f"Failed to enhance image: {str(e)}")
    
    def process_image_from_url(self, image_url: str, operation: str = "remove_background", **kwargs) -> bytes:
        """Process an image from a URL"""
        try:
            # Download the image first
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            image_data = img_response.content
            
            # Process based on operation type
            if operation == "remove_background":
                return self.remove_background(image_data, kwargs.get('format', 'PNG'))
            elif operation == "change_background":
                background_prompt = kwargs.get('background_prompt', 'white background')
                return self.change_background(image_data, background_prompt, kwargs.get('format', 'PNG'))
            elif operation == "enhance":
                return self.enhance_image(image_data, kwargs.get('format', 'PNG'))
            else:
                raise ValueError(f"Unsupported operation: {operation}")
        
        except Exception as e:
            raise Exception(f"Failed to process image from URL: {str(e)}")
    
    def batch_process_images(self, image_urls: list, operation: str = "remove_background", **kwargs) -> Dict[str, Any]:
        """Process multiple images in batch"""
        results = {
            'successful': [],
            'failed': [],
            'processed_images': {}
        }
        
        for i, url in enumerate(image_urls):
            try:
                processed_image = self.process_image_from_url(url, operation, **kwargs)
                results['successful'].append(url)
                results['processed_images'][url] = processed_image
                print(f"Successfully processed image {i+1}/{len(image_urls)}")
            except Exception as e:
                results['failed'].append({'url': url, 'error': str(e)})
                print(f"Failed to process image {i+1}/{len(image_urls)}: {str(e)}")
        
        return results
    
    def get_available_backgrounds(self) -> list:
        """Get list of available background options"""
        # Common background prompts that work well with PhotoRoom
        return [
            "white background",
            "black background",
            "transparent background",
            "gradient background",
            "studio lighting background",
            "natural outdoor background",
            "modern office background",
            "luxury background",
            "minimalist background",
            "colorful abstract background"
        ]