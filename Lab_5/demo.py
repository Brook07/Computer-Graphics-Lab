#!/usr/bin/env python3
"""
Lab 5 Visual Demo Generator
Generates all visual outputs for the 3D Transformations lab report
"""

import sys
import os

def install_packages():
    """Install required packages"""
    import subprocess
    
    packages = ['matplotlib', 'numpy', 'Pillow', 'PyOpenGL', 'PyOpenGL_accelerate']
    
    for package in packages:
        try:
            __import__(package.replace('-', '_').lower())
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_visual_demo():
    """Run the visual demonstration script"""
    print("="*60)
    print("Lab 5: 3D Transformations - Visual Output Generation")
    print("="*60)
    
    try:
        # Install packages if needed
        install_packages()
        
        # Import and run visual demo
        from visual_demo import generate_all_transformations
        generate_all_transformations()
        
        print("\\n" + "="*60)
        print("Visual outputs generated successfully!")
        print("Check the 'fig' directory for all generated images:")
        
        if os.path.exists('fig'):
            files = [f for f in os.listdir('fig') if f.endswith('.png')]
            for file in sorted(files):
                print(f"  - fig/{file}")
        
        print("\\nYou can now use these images in your Lab 5 report.")
        print("="*60)
        
    except Exception as e:
        print(f"Error generating visuals: {e}")
        print("Please make sure all dependencies are installed correctly.")

def print_controls():
    """Print OpenGL program controls"""
    print("\\nOpenGL Program Controls (main.py):")
    print("-" * 40)
    print("Transformations:")
    print("  t - Translation mode")
    print("  r - Rotation mode") 
    print("  s - Scale mode")
    print("  h - Shear mode")
    print("\\nAxes:")
    print("  x, y, z - Select axis")
    print("\\nShapes:")
    print("  1, 2, 3, 4 - Select shape (Cube, Sphere, Teapot, Torus)")
    print("\\nProjection:")
    print("  p - Toggle perspective/orthographic")
    print("\\nControls:")
    print("  ↑↓ - Increase/decrease transformation")
    print("  c - Cycle shear components (in shear mode)")
    print("  Space - Reset all transformations")
    print("  f - Take screenshot")
    print("  d - Capture demonstration sequences")
    print("  Esc - Exit")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_controls()
    else:
        run_visual_demo()
        print_controls()