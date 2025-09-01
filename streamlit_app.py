"""
Shopify-PhotoRoom Integration App
AI-powered batch image editing for Shopify products
"""
import streamlit as st
import pandas as pd
from PIL import Image
import io
from datetime import datetime
import os

from batch_processor import BatchProcessor
from photoroom_client import PhotoRoomClient
from config import SHOPIFY_SHOP_URL, SHOPIFY_ACCESS_TOKEN

# Page configuration
st.set_page_config(
    page_title="Shopify PhotoRoom Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'batch_processor' not in st.session_state:
    st.session_state.batch_processor = None
if 'product_images' not in st.session_state:
    st.session_state.product_images = []
if 'selected_images' not in st.session_state:
    st.session_state.selected_images = []
if 'processing_results' not in st.session_state:
    st.session_state.processing_results = None

def main():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 Shopify PhotoRoom Studio</h1>
        <p>AI-powered batch image editing for your Shopify products</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Shopify configuration
        st.subheader("Shopify Settings")
        shopify_url = st.text_input("Shopify Store URL", value=SHOPIFY_SHOP_URL, placeholder="your-store.myshopify.com")
        shopify_token = st.text_input("Shopify Access Token", value=SHOPIFY_ACCESS_TOKEN, type="password")
        
        if st.button("🔗 Connect to Shopify"):
            if shopify_url and shopify_token:
                try:
                    # Update environment variables
                    os.environ['SHOPIFY_SHOP_URL'] = shopify_url
                    os.environ['SHOPIFY_ACCESS_TOKEN'] = shopify_token
                    
                    # Initialize batch processor
                    st.session_state.batch_processor = BatchProcessor()
                    st.success("✅ Connected to Shopify successfully!")
                    
                    # Load product images
                    with st.spinner("Loading product images..."):
                        st.session_state.product_images = st.session_state.batch_processor.get_product_images_for_selection()
                    
                    st.success(f"📸 Loaded {len(st.session_state.product_images)} product images")
                    
                except Exception as e:
                    st.error(f"❌ Connection failed: {str(e)}")
            else:
                st.warning("Please provide both Shopify URL and Access Token")
    
    # Main content
    if st.session_state.batch_processor is None:
        st.info("👈 Please configure your Shopify connection in the sidebar to get started.")
        return
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Select Images", "🎨 Process Images", "📊 Results", "📈 History"])
    
    with tab1:
        st.header("Select Product Images")
        
        if not st.session_state.product_images:
            st.warning("No product images found. Please check your Shopify connection.")
            return
        
        # Create DataFrame for better display
        df = pd.DataFrame(st.session_state.product_images)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            product_filter = st.multiselect(
                "Filter by Product",
                options=df['product_title'].unique(),
                default=[]
            )
        
        with col2:
            max_images = st.slider("Max images to display", 10, 100, 50)
        
        # Apply filters
        filtered_df = df.copy()
        if product_filter:
            filtered_df = filtered_df[filtered_df['product_title'].isin(product_filter)]
        
        filtered_df = filtered_df.head(max_images)
        
        # Image selection
        st.subheader(f"Available Images ({len(filtered_df)})")
        
        # Select all/none buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select All Visible"):
                st.session_state.selected_images = filtered_df.to_dict('records')
        with col2:
            if st.button("Clear Selection"):
                st.session_state.selected_images = []
        
        # Display images with selection checkboxes
        selected_indices = []
        
        for idx, row in filtered_df.iterrows():
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                # Checkbox for selection
                is_selected = st.checkbox(f"Select", key=f"img_{idx}")
                if is_selected:
                    selected_indices.append(idx)
            
            with col2:
                # Image info
                st.write(f"**{row['product_title']}**")
                st.write(f"Image ID: {row['image_id']}")
                try:
                    st.image(row['image_url'], width=200)
                except:
                    st.write("Image preview not available")
            
            with col3:
                st.write(f"Product ID: {row['product_id']}")
        
        # Update selected images based on checkboxes
        if selected_indices:
            st.session_state.selected_images = filtered_df.iloc[selected_indices].to_dict('records')
        
        st.info(f"Selected {len(st.session_state.selected_images)} images for processing")
    
    with tab2:
        st.header("Process Selected Images")
        
        if not st.session_state.selected_images:
            st.warning("Please select images in the 'Select Images' tab first.")
            return
        
        st.success(f"Ready to process {len(st.session_state.selected_images)} selected images")
        
        # Processing options
        col1, col2 = st.columns(2)
        
        with col1:
            operation = st.selectbox(
                "Choose Operation",
                ["remove_background", "change_background", "enhance"],
                format_func=lambda x: {
                    "remove_background": "🗑️ Remove Background",
                    "change_background": "🎨 Change Background", 
                    "enhance": "✨ Enhance Image"
                }[x]
            )
        
        with col2:
            output_format = st.selectbox("Output Format", ["PNG", "JPG"])
        
        # Additional options based on operation
        additional_params = {}
        
        if operation == "change_background":
            photoroom_client = PhotoRoomClient()
            background_options = photoroom_client.get_available_backgrounds()
            
            background_choice = st.selectbox("Background Style", background_options)
            additional_params['background_prompt'] = background_choice
            
            # Custom background option
            if st.checkbox("Use custom background description"):
                custom_bg = st.text_input("Custom background description")
                if custom_bg:
                    additional_params['background_prompt'] = custom_bg
        
        additional_params['format'] = output_format
        
        # Processing controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start Processing", type="primary"):
                with st.spinner("Processing images... This may take a few minutes."):
                    try:
                        results = st.session_state.batch_processor.process_batch(
                            st.session_state.selected_images,
                            operation,
                            **additional_params
                        )
                        st.session_state.processing_results = results
                        st.success("✅ Processing completed!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Processing failed: {str(e)}")
        
        with col2:
            if st.session_state.processing_results and st.button("📤 Upload to Shopify"):
                with st.spinner("Uploading processed images to Shopify..."):
                    try:
                        upload_results = st.session_state.batch_processor.upload_processed_images_to_shopify(
                            st.session_state.processing_results['results'],
                            replace_original=st.checkbox("Replace original images", value=True)
                        )
                        st.success("✅ Upload completed!")
                        st.json(upload_results['summary'])
                    except Exception as e:
                        st.error(f"❌ Upload failed: {str(e)}")
    
    with tab3:
        st.header("Processing Results")
        
        if not st.session_state.processing_results:
            st.info("No processing results available. Please process some images first.")
            return
        
        results = st.session_state.processing_results
        summary = results['summary']
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Images", summary['total'])
        with col2:
            st.metric("Successful", summary['successful'])
        with col3:
            st.metric("Failed", summary['failed'])
        with col4:
            st.metric("Success Rate", f"{summary['success_rate']:.1f}%")
        
        # Detailed results
        st.subheader("Detailed Results")
        
        # Create results DataFrame
        results_data = []
        for result in results['results']:
            results_data.append({
                'Product ID': result.product_id,
                'Image ID': result.image_id,
                'Status': '✅ Success' if result.success else '❌ Failed',
                'Processing Time (s)': f"{result.processing_time:.2f}" if result.processing_time else "N/A",
                'Error': result.error_message if result.error_message else ""
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True)
        
        # Export results
        if st.button("📁 Export Results"):
            filename = st.session_state.batch_processor.export_results(results)
            st.success(f"Results exported to {filename}")
        
        # Show processed images preview
        st.subheader("Processed Images Preview")
        successful_results = [r for r in results['results'] if r.success and r.processed_data]
        
        cols = st.columns(min(4, len(successful_results)))
        for i, result in enumerate(successful_results[:8]):  # Show max 8 previews
            with cols[i % 4]:
                try:
                    image = Image.open(io.BytesIO(result.processed_data))
                    st.image(image, caption=f"Product {result.product_id}", width=150)
                except Exception as e:
                    st.write(f"Preview error: {str(e)}")
    
    with tab4:
        st.header("Processing History")
        
        history = st.session_state.batch_processor.get_processing_history()
        
        if not history:
            st.info("No processing history available.")
            return
        
        for i, session in enumerate(reversed(history)):
            with st.expander(f"Session {len(history)-i} - {session['summary']['timestamp'][:19]}"):
                summary = session['summary']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Images", summary['total'])
                with col2:
                    st.metric("Success Rate", f"{summary['success_rate']:.1f}%")
                with col3:
                    st.metric("Operation", summary['operation'].replace('_', ' ').title())
                
                st.write(f"**Processing Time:** {summary['total_processing_time']:.2f} seconds")

if __name__ == "__main__":
    main()
