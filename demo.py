#!/usr/bin/env python3
"""
Demo script for AI Saree Draping functionality
This script demonstrates the core computer vision techniques used in the application.
"""

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def create_sample_person_silhouette():
    """Create a simple person silhouette for demonstration"""
    # Create a blank image
    img = np.zeros((400, 300, 3), dtype=np.uint8)
    
    # Draw a simple person shape
    # Head
    cv2.circle(img, (150, 60), 25, (255, 255, 255), -1)
    
    # Body
    cv2.rectangle(img, (125, 85), (175, 200), (255, 255, 255), -1)
    
    # Arms
    cv2.rectangle(img, (100, 85), (125, 150), (255, 255, 255), -1)
    cv2.rectangle(img, (175, 85), (200, 150), (255, 255, 255), -1)
    
    # Legs
    cv2.rectangle(img, (135, 200), (155, 300), (255, 255, 255), -1)
    cv2.rectangle(img, (165, 200), (185, 300), (255, 255, 255), -1)
    
    return img

def demo_saree_draping():
    """Demonstrate saree draping on a sample silhouette"""
    print("🥻 AI Saree Draping Demo")
    print("=" * 40)
    
    # Create sample person
    person_img = create_sample_person_silhouette()
    
    # Simulate detected keypoints (normally from computer vision)
    keypoints = {
        'left_shoulder': (125, 85),
        'right_shoulder': (175, 85),
        'left_waist': (135, 140),
        'right_waist': (165, 140),
        'left_hip': (140, 180),
        'right_hip': (160, 180),
        'center_x': 150,
        'body_width': 50,
        'body_height': 115
    }
    
    # Create saree overlay
    overlay = np.zeros_like(person_img)
    
    # Saree color (pink)
    saree_color = (255, 182, 193)
    
    # Draw saree body
    left_waist = keypoints['left_waist']
    right_waist = keypoints['right_waist']
    left_hip = keypoints['left_hip']
    right_hip = keypoints['right_hip']
    
    # Main saree drape
    pts = np.array([left_waist, right_waist, right_hip, left_hip], np.int32)
    cv2.fillPoly(overlay, [pts], saree_color)
    
    # Pallu (decorative end)
    left_shoulder = keypoints['left_shoulder']
    pallu_points = [
        left_shoulder,
        (left_shoulder[0] - 30, left_shoulder[1] + 60),
        (left_shoulder[0] + 60, left_shoulder[1] + 120),
        (keypoints['center_x'], left_shoulder[1] + 30)
    ]
    
    pallu_pts = np.array(pallu_points, np.int32)
    cv2.fillPoly(overlay, [pallu_pts], saree_color)
    
    # Add border
    cv2.polylines(overlay, [pallu_pts], True, (200, 150, 150), 2)
    
    # Blend with original
    result = cv2.addWeighted(person_img, 0.4, overlay, 0.6, 0)
    
    print("✅ Saree draping simulation complete!")
    print("📊 Keypoints detected:")
    for name, point in keypoints.items():
        if isinstance(point, tuple):
            print(f"   {name}: {point}")
    
    print("\n🎨 Saree elements added:")
    print("   - Main drape (waist to hip)")
    print("   - Pallu (decorative end)")
    print("   - Border decoration")
    
    print(f"\n📐 Image dimensions: {person_img.shape}")
    print(f"🎨 Saree color (BGR): {saree_color}")
    
    return result, person_img, overlay

def main():
    """Main demo function"""
    try:
        result, original, overlay = demo_saree_draping()
        
        print("\n" + "=" * 40)
        print("🚀 Demo completed successfully!")
        print("💡 This demonstrates the core AI saree draping logic")
        print("🌐 Run 'streamlit run streamlit_app.py' for the full web interface")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()