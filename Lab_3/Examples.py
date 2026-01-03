"""
Example Usage and Test Cases for 2D Transformations
This file demonstrates how to use the 2D_Transformations module
"""

import importlib
import sys

# Import the module with hyphens in the name
transformations_module = importlib.import_module('2D_Transformations')
Shape2D = transformations_module.Shape2D
Transformation2D = transformations_module.Transformation2D
Visualizer2D = transformations_module.Visualizer2D

import numpy as np


def example_1_basic_translation():
    """Example 1: Basic Translation"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Translation")
    print("="*60)
    
    # Create a rectangle
    rect = Shape2D([(0, 0), (3, 0), (3, 2), (0, 2)], name="Rectangle")
    print(f"Original points:\n{rect.original_points}\n")
    
    # Translate by 5 units right and 2 units up
    trans = Transformation2D.translation_matrix(5, 2)
    rect.apply_transformation(trans)
    print(f"After translating (5, 2):\n{rect.current_points}\n")


def example_2_rotation_around_origin():
    """Example 2: Rotation around origin"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Rotation around Origin")
    print("="*60)
    
    # Create a square
    square = Shape2D([(1, 1), (3, 1), (3, 3), (1, 3)], name="Square")
    print(f"Original points:\n{square.original_points}\n")
    
    # Rotate 90 degrees counter-clockwise
    rot = Transformation2D.rotation_matrix(90)
    square.apply_transformation(rot)
    print(f"After rotating 90°:\n{square.current_points}\n")


def example_3_scaling():
    """Example 3: Scaling"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Scaling")
    print("="*60)
    
    # Create a triangle
    tri = Shape2D([(0, 0), (4, 0), (2, 4)], name="Triangle")
    print(f"Original points:\n{tri.original_points}\n")
    
    # Scale: 2x in X direction, 1.5x in Y direction
    scale = Transformation2D.scaling_matrix(2, 1.5)
    tri.apply_transformation(scale)
    print(f"After scaling (2x, 1.5x):\n{tri.current_points}\n")


def example_4_reflection():
    """Example 4: Reflection"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Reflection")
    print("="*60)
    
    # Create a triangle
    tri = Shape2D([(0, 0), (3, 0), (1.5, 2)], name="Triangle")
    print(f"Original points:\n{tri.original_points}\n")
    
    # Reflect about Y-axis
    ref = Transformation2D.reflection_matrix('y')
    tri.apply_transformation(ref)
    print(f"After reflection about Y-axis:\n{tri.current_points}\n")
    
    # Reflect about X-axis
    tri.reset()
    ref = Transformation2D.reflection_matrix('x')
    tri.apply_transformation(ref)
    print(f"After reflection about X-axis:\n{tri.current_points}\n")


def example_5_shearing():
    """Example 5: Shearing"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Shearing")
    print("="*60)
    
    # Create a square
    square = Shape2D([(0, 0), (2, 0), (2, 2), (0, 2)], name="Square")
    print(f"Original points:\n{square.original_points}\n")
    
    # Shear: shx=0.5 (shear in x based on y), shy=0 (no y shear)
    shear = Transformation2D.shearing_matrix(shx=0.5, shy=0)
    square.apply_transformation(shear)
    print(f"After shearing (shx=0.5):\n{square.current_points}\n")


def example_6_composite_transformation():
    """Example 6: Composite Transformations"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Composite Transformations")
    print("="*60)
    
    # Create a rectangle
    rect = Shape2D([(0, 0), (2, 0), (2, 1), (0, 1)], name="Rectangle")
    print(f"Original points:\n{rect.original_points}\n")
    
    # Step 1: Translate
    print("Step 1: Translate by (2, 1)")
    trans = Transformation2D.translation_matrix(2, 1)
    print(f"Translation matrix:\n{trans}\n")
    
    # Step 2: Rotate
    print("Step 2: Rotate by 45°")
    rot = Transformation2D.rotation_matrix(45)
    print(f"Rotation matrix:\n{rot}\n")
    
    # Step 3: Scale
    print("Step 3: Scale by (1.5, 1.5)")
    scale = Transformation2D.scaling_matrix(1.5, 1.5)
    print(f"Scaling matrix:\n{scale}\n")
    
    # Combine all transformations
    composite = Transformation2D.composite_transformation(scale, rot, trans)
    print(f"Composite Matrix (Applied as: Scale → Rotate → Translate):\n{composite}\n")
    
    rect.apply_transformation(composite)
    print(f"Final transformed points:\n{rect.current_points}\n")


def example_7_sequential_transformations():
    """Example 7: Sequential Transformations (apply one by one)"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Sequential Transformations")
    print("="*60)
    
    # Create a square
    square = Shape2D([(0, 0), (1, 0), (1, 1), (0, 1)], name="Square")
    print(f"Original points:\n{square.original_points}\n")
    
    # Apply translation
    print("Applied: Translation (2, 2)")
    trans = Transformation2D.translation_matrix(2, 2)
    square.apply_transformation(trans)
    print(f"Points after translation:\n{square.current_points}\n")
    
    # Apply rotation
    print("Applied: Rotation 30°")
    rot = Transformation2D.rotation_matrix(30)
    square.apply_transformation(rot)
    print(f"Points after rotation:\n{square.current_points}\n")
    
    # Apply scaling
    print("Applied: Scaling (2, 2)")
    scale = Transformation2D.scaling_matrix(2, 2)
    square.apply_transformation(scale)
    print(f"Final points:\n{square.current_points}\n")


def example_8_homogeneous_coordinates():
    """Example 8: Understanding Homogeneous Coordinates"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Homogeneous Coordinates")
    print("="*60)
    
    # Create a simple point
    line = Shape2D([(1, 2), (3, 4)], name="Line")
    print(f"2D Points:\n{line.current_points}\n")
    
    # Convert to homogeneous coordinates
    homo = line.get_homogeneous_points()
    print(f"Homogeneous Coordinates (added 1 as third element):\n{homo}\n")
    
    # Apply transformation to homogeneous coordinates
    trans = Transformation2D.translation_matrix(2, 3)
    print(f"Translation Matrix:\n{trans}\n")
    
    transformed_homo = (trans @ homo.T).T
    print(f"After transformation (still homogeneous):\n{transformed_homo}\n")
    
    # Convert back to 2D
    transformed_2d = transformed_homo[:, :2]
    print(f"Back to 2D coordinates:\n{transformed_2d}\n")


def example_9_verify_matrix_mathematics():
    """Example 9: Verify transformation mathematics"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Matrix Mathematics Verification")
    print("="*60)
    
    # Manual calculation
    print("Manual calculation for Translation (3, 2):")
    point_2d = np.array([1, 1])
    point_homo = np.array([1, 1, 1])
    print(f"Original 2D point: {point_2d}")
    print(f"Homogeneous form: {point_homo}\n")
    
    trans = Transformation2D.translation_matrix(3, 2)
    print(f"Translation matrix:\n{trans}\n")
    
    result_homo = trans @ point_homo
    print(f"Result (homogeneous): {result_homo}")
    print(f"Result (2D): {result_homo[:2]}\n")
    
    # Using the Shape class
    print("Using Shape2D class:")
    line = Shape2D([(1, 1)], name="Point")
    line.apply_transformation(trans)
    print(f"Result: {line.current_points[0]}\n")
    
    print("✓ Both methods produce the same result!")


def run_all_examples():
    """Run all examples"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           2D TRANSFORMATIONS - EXAMPLE USAGE               ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    example_1_basic_translation()
    example_2_rotation_around_origin()
    example_3_scaling()
    example_4_reflection()
    example_5_shearing()
    example_6_composite_transformation()
    example_7_sequential_transformations()
    example_8_homogeneous_coordinates()
    example_9_verify_matrix_mathematics()
    
    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_examples()
