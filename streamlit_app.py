import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage
import io

# Configure page
st.set_page_config(
    page_title="AI Saree Draping Assistant",
    page_icon="🥻",
    layout="wide",
    initial_sidebar_state="expanded"
)

class SareeDrapingAI:
    def __init__(self):
        self.image = None
        self.processed_image = None
        
    def detect_body_regions(self, image):
        """Simplified body detection using image processing"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Use edge detection to find contours
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (assuming it's the person)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Estimate body regions based on proportions
                height, width = image.shape[:2]
                
                # Approximate body keypoints based on human proportions
                center_x = x + w // 2
                
                # Head region (top 1/8 of body)
                head_y = y + h // 8
                
                # Shoulder region (about 1/6 down from head)
                shoulder_y = y + h // 4
                left_shoulder = (center_x - w // 4, shoulder_y)
                right_shoulder = (center_x + w // 4, shoulder_y)
                
                # Waist region (about 1/2 down from top)
                waist_y = y + h // 2
                left_waist = (center_x - w // 6, waist_y)
                right_waist = (center_x + w // 6, waist_y)
                
                # Hip region (about 2/3 down from top)
                hip_y = y + int(h * 0.65)
                left_hip = (center_x - w // 5, hip_y)
                right_hip = (center_x + w // 5, hip_y)
                
                keypoints = {
                    'left_shoulder': left_shoulder,
                    'right_shoulder': right_shoulder,
                    'left_waist': left_waist,
                    'right_waist': right_waist,
                    'left_hip': left_hip,
                    'right_hip': right_hip,
                    'center_x': center_x,
                    'body_width': w,
                    'body_height': h
                }
                
                return keypoints
            
        except Exception as e:
            st.error(f"Error in body detection: {str(e)}")
            return None
        
        return None
    
    def create_saree_overlay(self, keypoints, style="Nivi", color=(255, 182, 193), pattern="solid"):
        """Create saree overlay based on detected body regions"""
        if not keypoints:
            return None
            
        overlay = np.zeros_like(self.image)
        
        # Create saree pleats at waist
        self.draw_saree_pleats(overlay, keypoints, color)
        
        # Create pallu (the decorative end)
        self.draw_pallu(overlay, keypoints, style, color)
        
        # Add border patterns
        if pattern != "solid":
            self.add_saree_border(overlay, keypoints, pattern)
            
        return overlay
    
    def draw_saree_pleats(self, overlay, keypoints, color):
        """Draw saree pleats at the waist"""
        left_waist = keypoints['left_waist']
        right_waist = keypoints['right_waist']
        left_hip = keypoints['left_hip']
        right_hip = keypoints['right_hip']
        
        # Draw main drape from waist to hip
        pts = np.array([left_waist, right_waist, right_hip, left_hip], np.int32)
        cv2.fillPoly(overlay, [pts], color)
        
        # Add pleats effect
        pleat_width = abs(right_waist[0] - left_waist[0]) // 8
        for i in range(3, 8):
            x = left_waist[0] + i * pleat_width
            cv2.line(overlay, (x, left_waist[1]), (x, left_hip[1]), 
                    (color[0]//2, color[1]//2, color[2]//2), 2)
        
        # Add bottom portion of saree
        body_bottom = keypoints['left_hip'][1] + keypoints['body_height'] // 4
        bottom_left = (left_hip[0], body_bottom)
        bottom_right = (right_hip[0], body_bottom)
        
        bottom_pts = np.array([left_hip, right_hip, bottom_right, bottom_left], np.int32)
        cv2.fillPoly(overlay, [bottom_pts], color)
    
    def draw_pallu(self, overlay, keypoints, style, color):
        """Draw saree pallu (decorative end)"""
        left_shoulder = keypoints['left_shoulder']
        right_shoulder = keypoints['right_shoulder']
        center_x = keypoints['center_x']
        
        if style == "Nivi":
            # Traditional Nivi style pallu
            pallu_points = [
                left_shoulder,
                (left_shoulder[0] - 50, left_shoulder[1] + 100),
                (left_shoulder[0] + 100, left_shoulder[1] + 200),
                (center_x, left_shoulder[1] + 50)
            ]
        elif style == "Bengali":
            # Bengali style pallu
            pallu_points = [
                left_shoulder,
                (left_shoulder[0] - 30, left_shoulder[1] + 80),
                (left_shoulder[0] + 80, left_shoulder[1] + 150),
                right_shoulder
            ]
        elif style == "Gujarati":
            # Gujarati style pallu
            pallu_points = [
                right_shoulder,
                (right_shoulder[0] + 30, right_shoulder[1] + 60),
                (right_shoulder[0] + 60, right_shoulder[1] + 120),
                (center_x + 20, right_shoulder[1] + 40)
            ]
        else:  # South Indian style
            pallu_points = [
                left_shoulder,
                (left_shoulder[0] - 40, left_shoulder[1] + 60),
                (left_shoulder[0] + 60, left_shoulder[1] + 140),
                (left_shoulder[0] + 80, left_shoulder[1] + 30)
            ]
        
        pts = np.array(pallu_points, np.int32)
        cv2.fillPoly(overlay, [pts], color)
        
        # Add pallu border
        border_color = (color[0]//3, color[1]//3, color[2]//3)
        cv2.polylines(overlay, [pts], True, border_color, 3)
        
        # Add decorative elements to pallu
        if len(pallu_points) >= 3:
            center_pallu = pallu_points[1]
            cv2.circle(overlay, center_pallu, 15, border_color, -1)
    
    def add_saree_border(self, overlay, keypoints, pattern):
        """Add decorative border patterns"""
        border_color = (255, 215, 0)  # Gold color for borders
        
        if pattern == "floral":
            # Add floral pattern (circles and small decorations)
            for i, point in enumerate([keypoints['left_waist'], keypoints['right_waist'], 
                                     keypoints['left_hip'], keypoints['right_hip']]):
                cv2.circle(overlay, point, 10, border_color, -1)
                # Add small petals around
                for angle in range(0, 360, 60):
                    x = int(point[0] + 15 * np.cos(np.radians(angle)))
                    y = int(point[1] + 15 * np.sin(np.radians(angle)))
                    cv2.circle(overlay, (x, y), 3, border_color, -1)
                    
        elif pattern == "geometric":
            # Add geometric patterns
            for i, point in enumerate([keypoints['left_waist'], keypoints['right_waist']]):
                # Draw diamond pattern
                diamond_size = 12
                diamond_pts = np.array([
                    [point[0], point[1] - diamond_size],
                    [point[0] + diamond_size, point[1]],
                    [point[0], point[1] + diamond_size],
                    [point[0] - diamond_size, point[1]]
                ], np.int32)
                cv2.fillPoly(overlay, [diamond_pts], border_color)
    
    def blend_saree_with_image(self, overlay, alpha=0.6):
        """Blend saree overlay with original image"""
        return cv2.addWeighted(self.image, 1-alpha, overlay, alpha, 0)

def main():
    st.title("🥻 AI Saree Draping Assistant")
    st.markdown("### Transform your photos with AI-powered virtual saree draping!")
    
    # Add info about the simplified version
    st.info("📝 **Note**: This is a simplified version using computer vision techniques. For best results, use photos with clear body silhouettes against contrasting backgrounds.")
    
    # Sidebar for controls
    st.sidebar.header("Saree Customization")
    
    # Saree style selection
    draping_style = st.sidebar.selectbox(
        "Select Draping Style",
        ["Nivi", "Bengali", "Gujarati", "South Indian"],
        help="Choose from traditional regional draping styles"
    )
    
    # Color selection
    color_option = st.sidebar.selectbox(
        "Choose Color",
        ["Pink", "Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Maroon", "Navy"]
    )
    
    color_map = {
        "Pink": (255, 182, 193),
        "Red": (255, 0, 0),
        "Blue": (0, 0, 255),
        "Green": (0, 255, 0),
        "Yellow": (255, 255, 0),
        "Purple": (128, 0, 128),
        "Orange": (255, 165, 0),
        "Maroon": (128, 0, 0),
        "Navy": (0, 0, 128)
    }
    
    # Pattern selection
    pattern = st.sidebar.selectbox(
        "Border Pattern",
        ["solid", "floral", "geometric"],
        help="Add decorative patterns to the saree border"
    )
    
    # Transparency control
    alpha = st.sidebar.slider("Saree Transparency", 0.3, 0.9, 0.6, 0.1, 
                             help="Adjust the opacity of the virtual saree")
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Upload Your Photo")
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a photo where you're standing straight facing the camera"
        )
        
        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_column_width=True)
    
    with col2:
        st.header("AI Draped Result")
        
        if uploaded_file is not None:
            # Process the image
            with st.spinner("AI is draping the saree..."):
                try:
                    # Convert PIL to OpenCV format
                    image_array = np.array(image)
                    cv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                    
                    # Initialize AI draper
                    draper = SareeDrapingAI()
                    draper.image = cv_image
                    
                    # Detect body regions
                    keypoints = draper.detect_body_regions(cv_image)
                    
                    if keypoints:
                        # Create saree overlay
                        overlay = draper.create_saree_overlay(
                            keypoints,
                            style=draping_style,
                            color=color_map[color_option],
                            pattern=pattern
                        )
                        
                        if overlay is not None:
                            # Blend with original image
                            result = draper.blend_saree_with_image(overlay, alpha)
                            
                            # Convert back to RGB for display
                            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                            
                            # Display result
                            st.image(result_rgb, caption=f"AI Draped Saree ({draping_style} Style)", use_column_width=True)
                            
                            # Download button
                            result_pil = Image.fromarray(result_rgb)
                            buf = io.BytesIO()
                            result_pil.save(buf, format="PNG")
                            byte_im = buf.getvalue()
                            
                            st.download_button(
                                label="📥 Download Result",
                                data=byte_im,
                                file_name=f"saree_draped_{draping_style.lower()}_style.png",
                                mime="image/png"
                            )
                            
                            # Show detected keypoints option
                            if st.checkbox("Show Detected Body Points"):
                                debug_image = cv_image.copy()
                                for name, point in keypoints.items():
                                    if isinstance(point, tuple):
                                        cv2.circle(debug_image, point, 5, (0, 255, 0), -1)
                                        cv2.putText(debug_image, name, (point[0]+10, point[1]), 
                                                  cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
                                
                                debug_rgb = cv2.cvtColor(debug_image, cv2.COLOR_BGR2RGB)
                                st.image(debug_rgb, caption="Detected Body Points", use_column_width=True)
                        else:
                            st.error("Failed to create saree overlay. Please try with a different image.")
                    else:
                        st.error("Could not detect body regions in the image. Please try with a clearer photo where you're standing straight facing the camera.")
                        
                except Exception as e:
                    st.error(f"An error occurred while processing the image: {str(e)}")
                    st.info("Please try with a different image or check if the image format is supported.")
    
    # Information section
    st.markdown("---")
    st.header("How it works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **1. Body Detection**
        - AI analyzes image contours
        - Identifies body silhouette
        - Estimates key body regions
        """)
    
    with col2:
        st.markdown("""
        **2. Saree Simulation**
        - Creates virtual saree overlay
        - Applies traditional draping styles
        - Adds realistic fabric effects
        """)
    
    with col3:
        st.markdown("""
        **3. Style Customization**
        - Choose from various styles
        - Select colors and patterns
        - Adjust transparency and fit
        """)
    
    # Tips section
    st.markdown("---")
    st.header("📸 Tips for Best Results")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **Photo Guidelines:**
        - Stand straight facing the camera
        - Good lighting is essential
        - Wear fitted clothing for better detection
        - Clear background preferred
        - Avoid loose or baggy clothing
        """)
    
    with tips_col2:
        st.markdown("""
        **Styling Tips:**
        - Try different draping styles
        - Experiment with colors
        - Adjust transparency for realism
        - Use patterns for festive occasions
        - Check detected points for accuracy
        """)
    
    # Style information
    st.markdown("---")
    st.header("🎨 Draping Styles Information")
    
    style_col1, style_col2 = st.columns(2)
    
    with style_col1:
        st.markdown("""
        **Nivi Style (Andhra Pradesh)**
        - Most popular and widely worn
        - Pleats at the front
        - Pallu over left shoulder
        
        **Bengali Style (West Bengal)**
        - Traditional red and white
        - Distinctive pleating style
        - Pallu brought from back to front
        """)
    
    with style_col2:
        st.markdown("""
        **Gujarati Style (Gujarat)**
        - Pallu in the front
        - Unique draping pattern
        - Often in vibrant colors
        
        **South Indian Style**
        - Traditional temple draping
        - More coverage
        - Elegant and formal appearance
        """)

if __name__ == "__main__":
    main()
