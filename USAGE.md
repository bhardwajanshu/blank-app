# 🥻 AI Saree Draping Assistant - Usage Guide

Welcome to the AI Saree Draping Assistant! This application uses computer vision and artificial intelligence to virtually drape sarees on photos.

## 🚀 Quick Start

### Method 1: Using the Launch Script (Recommended)
```bash
./run_app.sh
```

### Method 2: Manual Start
```bash
# Activate virtual environment
source saree_env/bin/activate

# Run the application
streamlit run streamlit_app.py
```

### Method 3: Demo Script (Testing)
```bash
# Test core functionality
source saree_env/bin/activate
python3 demo.py
```

## 📱 How to Use the Web Application

1. **Open your browser** and navigate to `http://localhost:8501`

2. **Upload Your Photo**:
   - Click "Choose an image..." in the left column
   - Select a photo where you're standing straight facing the camera
   - Supported formats: JPG, JPEG, PNG

3. **Customize Your Saree**:
   - **Draping Style**: Choose from Nivi, Bengali, Gujarati, or South Indian
   - **Color**: Select from 9 available colors
   - **Border Pattern**: Choose solid, floral, or geometric patterns
   - **Transparency**: Adjust the opacity of the virtual saree

4. **View Results**:
   - The AI will process your image and show the draped saree
   - You can download the result as a PNG file
   - Optional: Check "Show Detected Body Points" to see how the AI detected your body

## 🎯 Tips for Best Results

### Photo Guidelines
- **Good lighting** is essential for accurate body detection
- **Stand straight** facing the camera directly
- **Wear fitted clothing** (avoid loose, baggy clothes)
- **Clear background** helps with better detection
- **Avoid cluttered backgrounds** or busy patterns
- **High resolution** images work better

### What Works Best
- Full body shots
- Contrasting clothing against background
- Standing poses (not sitting or lying down)
- Front-facing photos
- Well-lit environments

### What to Avoid
- Side profiles or angled poses
- Very dark or poorly lit photos
- Busy, cluttered backgrounds
- Oversized or loose clothing
- Photos where the full body isn't visible

## 🎨 Available Draping Styles

### Nivi Style (Andhra Pradesh)
- Most popular and widely worn style
- Pleats at the front
- Pallu (decorative end) over left shoulder
- Modern and elegant appearance

### Bengali Style (West Bengal)
- Traditional red and white colors
- Distinctive pleating style
- Pallu brought from back to front
- Cultural and ceremonial appearance

### Gujarati Style (Gujarat)
- Pallu in the front
- Unique draping pattern
- Often in vibrant colors
- Festive and colorful look

### South Indian Style
- Traditional temple draping
- More coverage and modesty
- Elegant and formal appearance
- Classic and timeless style

## 🛠️ Technical Features

### AI Detection
- **Body Region Detection**: Uses OpenCV edge detection and contour analysis
- **Proportion-Based Estimation**: Estimates body keypoints using human anatomical proportions
- **Automatic Fitting**: Adapts saree placement to detected body shape

### Saree Simulation
- **Realistic Draping**: Simulates fabric flow and pleating
- **Style-Specific Patterns**: Each style has unique draping characteristics
- **Color Customization**: 9 predefined colors with proper blending
- **Pattern Overlay**: Floral and geometric border patterns

### Image Processing
- **Seamless Blending**: Alpha blending for realistic fabric appearance
- **Edge Enhancement**: Clean borders and decorative elements
- **High Quality Output**: Maintains original image resolution

## 🔧 Troubleshooting

### Common Issues

**"Could not detect body regions"**
- Try a photo with better lighting
- Ensure you're standing straight facing the camera
- Use a clearer background
- Make sure your full body is visible

**"Failed to create saree overlay"**
- The detected body points might be incorrect
- Try a different photo angle
- Ensure the image is not corrupted

**Application won't start**
- Make sure you're in the correct directory
- Check if the virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Slow processing**
- Large images take more time to process
- Consider resizing very large images
- Close other applications to free up memory

### Getting Help
1. Check the "Show Detected Body Points" option to see if detection is accurate
2. Try the demo script: `python3 demo.py` to test core functionality
3. Ensure all packages are installed correctly
4. Check that your image meets the photo guidelines

## 📁 Project Structure

```
.
├── streamlit_app.py       # Main web application
├── demo.py               # Demo script for testing
├── run_app.sh            # Launch script
├── requirements.txt      # Python dependencies
├── README.md            # Project overview
├── USAGE.md             # This usage guide
├── LICENSE              # License information
└── saree_env/           # Virtual environment
```

## 🐛 Known Limitations

- Works best with clear, well-lit photos
- Simplified body detection (not as advanced as MediaPipe)
- Saree simulation is artistic interpretation, not photorealistic
- Best results with front-facing poses
- Limited to predefined saree styles and colors

## 🔮 Future Enhancements

- Integration with advanced pose detection models
- More regional draping styles
- Custom color picker
- Fabric texture simulation
- Video processing capabilities
- 3D draping visualization
- Mobile app version

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Streamlit team for the web framework
- Traditional Indian textile artisans for inspiration
- Contributors and users for feedback and testing

---

**Made with ❤️ for preserving and celebrating traditional Indian fashion through modern AI technology**