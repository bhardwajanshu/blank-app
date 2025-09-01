"""
Configuration management for the Shopify-PhotoRoom integration app
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PhotoRoom API Configuration
PHOTOROOM_API_KEY = "sk_pr_replit_bd7865869cf23db4c22e5fa535262e0d92b3ed70"
PHOTOROOM_BASE_URL = "https://sdk.photoroom.com/v1"

# Shopify API Configuration
SHOPIFY_SHOP_URL = os.getenv("SHOPIFY_SHOP_URL", "")  # e.g., "your-store.myshopify.com"
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOPIFY_API_VERSION = "2024-01"

# App Configuration
MAX_BATCH_SIZE = 10
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']