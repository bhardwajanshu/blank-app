# 🥻 AI Saree Draping Assistant

An intelligent web application that uses AI and computer vision to virtually drape sarees on user photos. The application leverages MediaPipe for pose detection and OpenCV for image processing to create realistic saree overlays.

## ✨ Features

- **AI-Powered Pose Detection**: Uses MediaPipe to accurately detect body pose and key points
- **Multiple Draping Styles**: Support for traditional styles like Nivi, Bengali, Gujarati, and South Indian
- **Color Customization**: Choose from various saree colors (Pink, Red, Blue, Green, Yellow, Purple, Orange)
- **Pattern Options**: Add decorative borders with solid, floral, or geometric patterns
- **Adjustable Transparency**: Control the opacity of the virtual saree for realistic effects
- **Download Results**: Save the draped images in high quality PNG format
- **Real-time Processing**: Instant visualization of saree draping on uploaded photos

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd saree-draping-ai
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

4. Open your web browser and navigate to `http://localhost:8501`

## 📱 How to Use

1. **Upload Your Photo**: Click on "Choose an image..." to upload a clear photo where you're standing straight facing the camera
2. **Customize Your Saree**: Use the sidebar to:
   - Select draping style (Nivi, Bengali, etc.)
   - Choose saree color
   - Pick border patterns
   - Adjust transparency
3. **View Results**: The AI will process your image and show the draped saree result
4. **Download**: Click "Download Result" to save your draped image

## 🎯 Best Results Tips

### Photo Guidelines:
- Stand straight facing the camera
- Ensure good lighting
- Wear fitted clothing for better pose detection
- Use a clear background when possible
- Avoid loose or baggy clothing that might interfere with pose detection

### Styling Tips:
- Experiment with different draping styles to find your preference
- Try various colors to match occasions
- Adjust transparency for more realistic fabric appearance
- Use patterned borders for festive or special occasions

## 🔧 Technical Details

### AI Models Used:
- **MediaPipe Pose**: For human pose estimation and landmark detection
- **OpenCV**: For image processing and computer vision operations

### Key Components:
- **Pose Detection**: Identifies 33 body landmarks for accurate saree placement
- **Saree Overlay Generation**: Creates virtual fabric overlays based on detected body points
- **Style Algorithms**: Implements traditional draping patterns for different regional styles
- **Blending Engine**: Seamlessly combines virtual saree with original photo

### Supported Draping Styles:
- **Nivi Style**: Traditional Andhra Pradesh style with pleats at the front
- **Bengali Style**: Characteristic draping from West Bengal
- **Gujarati Style**: Traditional Gujarat regional draping
- **South Indian Style**: Classic South Indian temple draping

## 🛠️ Technical Architecture

```
User Photo Upload
       ↓
MediaPipe Pose Detection
       ↓
Extract Key Body Points
       ↓
Generate Saree Overlay
       ↓
Apply Style & Patterns
       ↓
Blend with Original Image
       ↓
Display Result
```

## 📦 Dependencies

- `streamlit`: Web application framework
- `opencv-python`: Computer vision library
- `mediapipe`: Google's ML framework for pose detection
- `numpy`: Numerical computing
- `pillow`: Image processing
- `matplotlib`: Plotting library
- `scipy`: Scientific computing
- `scikit-image`: Image processing algorithms

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MediaPipe team at Google for the pose detection model
- OpenCV community for computer vision tools
- Streamlit team for the web framework
- Traditional Indian textile artisans for inspiration on draping styles

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Ensure your photo meets the guidelines
3. Verify all dependencies are properly installed
4. Try with different images to isolate the issue

## 🔮 Future Enhancements

- Support for more regional draping styles
- Advanced fabric texture simulation
- 3D draping visualization
- Video processing capabilities
- Custom pattern designer
- Social sharing features

---

**Made with ❤️ for preserving and celebrating traditional Indian fashion through modern AI technology**
