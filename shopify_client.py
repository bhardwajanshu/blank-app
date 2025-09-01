"""
Shopify API client for fetching and updating product images
"""
import requests
import json
from typing import List, Dict, Optional
from config import SHOPIFY_SHOP_URL, SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_VERSION


class ShopifyClient:
    def __init__(self):
        self.shop_url = SHOPIFY_SHOP_URL
        self.access_token = SHOPIFY_ACCESS_TOKEN
        self.api_version = SHOPIFY_API_VERSION
        self.base_url = f"https://{self.shop_url}/admin/api/{self.api_version}"
        
        if not self.shop_url or not self.access_token:
            raise ValueError("Shopify shop URL and access token must be provided")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make a request to the Shopify API"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json'
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Shopify API request failed: {str(e)}")
    
    def get_products(self, limit: int = 250) -> List[Dict]:
        """Fetch all products from Shopify"""
        products = []
        params = f"?limit={limit}"
        
        try:
            response = self._make_request('GET', f'products.json{params}')
            products.extend(response.get('products', []))
            
            # Handle pagination if needed
            while len(response.get('products', [])) == limit:
                last_product_id = response['products'][-1]['id']
                params = f"?limit={limit}&since_id={last_product_id}"
                response = self._make_request('GET', f'products.json{params}')
                if response.get('products'):
                    products.extend(response['products'])
                else:
                    break
            
            return products
        except Exception as e:
            raise Exception(f"Failed to fetch products: {str(e)}")
    
    def get_product_images(self, product_id: int) -> List[Dict]:
        """Get all images for a specific product"""
        try:
            response = self._make_request('GET', f'products/{product_id}/images.json')
            return response.get('images', [])
        except Exception as e:
            raise Exception(f"Failed to fetch product images: {str(e)}")
    
    def upload_image_to_product(self, product_id: int, image_data: bytes, filename: str, alt_text: str = "") -> Dict:
        """Upload a new image to a product"""
        import base64
        
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        data = {
            "image": {
                "attachment": image_b64,
                "filename": filename,
                "alt": alt_text
            }
        }
        
        try:
            response = self._make_request('POST', f'products/{product_id}/images.json', data)
            return response.get('image', {})
        except Exception as e:
            raise Exception(f"Failed to upload image: {str(e)}")
    
    def update_product_image(self, product_id: int, image_id: int, image_data: bytes, filename: str) -> Dict:
        """Update an existing product image"""
        import base64
        
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        data = {
            "image": {
                "id": image_id,
                "attachment": image_b64,
                "filename": filename
            }
        }
        
        try:
            response = self._make_request('PUT', f'products/{product_id}/images/{image_id}.json', data)
            return response.get('image', {})
        except Exception as e:
            raise Exception(f"Failed to update image: {str(e)}")
    
    def get_all_product_images(self) -> List[Dict]:
        """Get all product images with product information"""
        all_images = []
        products = self.get_products()
        
        for product in products:
            product_images = product.get('images', [])
            for image in product_images:
                image_info = {
                    'product_id': product['id'],
                    'product_title': product['title'],
                    'image_id': image['id'],
                    'image_url': image['src'],
                    'alt_text': image.get('alt', ''),
                    'filename': image.get('src', '').split('/')[-1]
                }
                all_images.append(image_info)
        
        return all_images