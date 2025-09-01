# Shopify PhotoRoom Studio

An AI-powered batch image editing application that connects to your Shopify store and uses PhotoRoom's AI API to automatically process product images with background removal, background changes, and image enhancement.

## Features

🎨 **AI-Powered Image Editing**
- Remove backgrounds from product images
- Change backgrounds with AI-generated styles
- Enhance image quality automatically

📦 **Shopify Integration**
- Connect directly to your Shopify store
- Fetch all product images automatically
- Upload processed images back to Shopify

🚀 **Batch Processing**
- Process multiple images simultaneously
- Parallel processing for faster results
- Progress tracking and error handling

📊 **Results Dashboard**
- View processing results and statistics
- Preview processed images
- Export results to JSON

📈 **Processing History**
- Track all processing sessions
- Performance metrics and analytics

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Shopify API**
   - Create a custom app in your Shopify admin
   - Generate an Admin API access token with `read_products` and `write_products` permissions
   - Copy your store URL (e.g., `your-store.myshopify.com`) and access token

3. **Run the Application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Configure in the App**
   - Enter your Shopify store URL and access token in the sidebar
   - Click "Connect to Shopify" to load your product images

## Usage

### Step 1: Select Images
- Browse and filter your product images
- Select individual images or use "Select All"
- Preview images before processing

### Step 2: Process Images
- Choose operation type:
  - **Remove Background**: Clean background removal
  - **Change Background**: AI-generated backgrounds
  - **Enhance**: Improve image quality
- Configure additional settings (format, background style)
- Start batch processing

### Step 3: Review Results
- View processing statistics and success rates
- Preview processed images
- Export results for record-keeping

### Step 4: Upload to Shopify
- Upload processed images back to your store
- Choose to replace original images or create new ones
- Track upload success rates

## PhotoRoom API Features

The app leverages PhotoRoom's powerful AI capabilities:

- **Background Removal**: Professional-quality background removal
- **Background Generation**: AI-generated backgrounds from text prompts
- **Image Enhancement**: Automatic quality improvements
- **Batch Processing**: Handle multiple images efficiently

## API Configuration

### PhotoRoom API
The PhotoRoom API key is pre-configured in the application:
```
sk_pr_replit_bd7865869cf23db4c22e5fa535262e0d92b3ed70
```

### Shopify API
You'll need to provide:
- **Store URL**: your-store.myshopify.com
- **Access Token**: Generated from your Shopify admin

## Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Image Processing**: PhotoRoom AI API
- **E-commerce Integration**: Shopify Admin API
- **Batch Processing**: Parallel processing with ThreadPoolExecutor

### File Structure
```
├── streamlit_app.py       # Main Streamlit application
├── config.py             # Configuration management
├── shopify_client.py     # Shopify API integration
├── photoroom_client.py   # PhotoRoom API integration
├── batch_processor.py    # Batch processing logic
├── requirements.txt      # Python dependencies
└── .env.example         # Environment variables template
```

### Key Features
- **Error Handling**: Comprehensive error handling and recovery
- **Progress Tracking**: Real-time progress updates
- **Session Management**: Persistent session state
- **Export Functionality**: JSON export of processing results
- **Image Preview**: Before and after image comparisons

## Troubleshooting

### Common Issues

1. **Shopify Connection Failed**
   - Verify your store URL format (include .myshopify.com)
   - Check your access token permissions
   - Ensure your app has the required scopes

2. **PhotoRoom Processing Errors**
   - Check image format compatibility
   - Verify image URLs are accessible
   - Monitor API rate limits

3. **Upload Failures**
   - Ensure write permissions on your Shopify app
   - Check image size limits
   - Verify network connectivity

### Performance Tips

- Process images in smaller batches for better reliability
- Use PNG format for images with transparency
- Monitor processing times and adjust batch sizes accordingly

## Support

For issues related to:
- **Shopify API**: Check Shopify's API documentation
- **PhotoRoom API**: Refer to PhotoRoom's developer resources
- **Application Issues**: Check the error messages in the Results tab

## Security Notes

- API keys are handled securely within the application
- Shopify tokens are stored in session state only
- No sensitive data is permanently stored

---

Built with ❤️ using Streamlit, Shopify Admin API, and PhotoRoom AI API.