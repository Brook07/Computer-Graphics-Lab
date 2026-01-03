"""
2D Transformations using Homogeneous Coordinate Systems
Computer Graphics Lab Assignment

This program implements:
- 2D Translation
- 2D Rotation
- 2D Scaling
- 2D Reflection
- 2D Shearing
- Composite Transformations (Multiple transformations combined)

Author: Computer Graphics Lab
Date: 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math


class Shape2D:
    """
    A class to represent 2D shapes and apply transformations using homogeneous coordinates.
    Points are stored as homogeneous coordinates (x, y, 1).
    """
    
    def __init__(self, points, name="Shape"):
        """
        Initialize a 2D shape with given points.
        
        Args:
            points: List of (x, y) tuples representing vertices
            name: Name of the shape
        """
        self.name = name
        self.original_points = np.array(points, dtype=float)
        self.current_points = np.array(points, dtype=float)
        
    def get_homogeneous_points(self, points=None):
        """
        Convert 2D points to homogeneous coordinates (x, y, 1).
        
        Args:
            points: Points to convert (uses current_points if None)
            
        Returns:
            Array of homogeneous coordinates with shape (n, 3)
        """
        if points is None:
            points = self.current_points
        ones = np.ones((points.shape[0], 1))
        return np.hstack([points, ones])
    
    def apply_transformation(self, transformation_matrix):
        """
        Apply a transformation matrix to the current shape points.
        
        Args:
            transformation_matrix: 3x3 transformation matrix
        """
        homo_points = self.get_homogeneous_points()
        transformed_homo = (transformation_matrix @ homo_points.T).T
        self.current_points = transformed_homo[:, :2]
    
    def reset(self):
        """Reset the shape to its original position."""
        self.current_points = self.original_points.copy()


class Transformation2D:
    """
    A class to generate 2D transformation matrices using homogeneous coordinates.
    All matrices are 3x3 for compatibility with homogeneous coordinates.
    """
    
    @staticmethod
    def translation_matrix(tx, ty):
        """
        Create a translation transformation matrix.
        
        Args:
            tx: Translation in x-axis
            ty: Translation in y-axis
            
        Returns:
            3x3 translation matrix
        """
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ], dtype=float)
    
    @staticmethod
    def rotation_matrix(angle_degrees):
        """
        Create a rotation transformation matrix.
        
        Args:
            angle_degrees: Rotation angle in degrees (counter-clockwise)
            
        Returns:
            3x3 rotation matrix
        """
        angle_radians = math.radians(angle_degrees)
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)
        
        return np.array([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ], dtype=float)
    
    @staticmethod
    def scaling_matrix(sx, sy):
        """
        Create a scaling transformation matrix.
        
        Args:
            sx: Scaling factor in x-axis
            sy: Scaling factor in y-axis
            
        Returns:
            3x3 scaling matrix
        """
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ], dtype=float)
    
    @staticmethod
    def reflection_matrix(axis='x'):
        """
        Create a reflection transformation matrix.
        
        Args:
            axis: 'x' for reflection about x-axis, 'y' for y-axis, 'origin' for origin
            
        Returns:
            3x3 reflection matrix
        """
        if axis == 'x':
            # Reflection about x-axis
            return np.array([
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
            ], dtype=float)
        elif axis == 'y':
            # Reflection about y-axis
            return np.array([
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ], dtype=float)
        elif axis == 'origin':
            # Reflection about origin
            return np.array([
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
            ], dtype=float)
        else:
            raise ValueError("axis must be 'x', 'y', or 'origin'")
    
    @staticmethod
    def shearing_matrix(shx=0, shy=0):
        """
        Create a shearing transformation matrix.
        
        Args:
            shx: Shearing factor in x-direction
            shy: Shearing factor in y-direction
            
        Returns:
            3x3 shearing matrix
        """
        return np.array([
            [1, shx, 0],
            [shy, 1, 0],
            [0, 0, 1]
        ], dtype=float)
    
    @staticmethod
    def composite_transformation(*matrices):
        """
        Combine multiple transformation matrices into a single composite matrix.
        Matrices are applied left to right (first matrix is applied first).
        
        Args:
            *matrices: Variable number of 3x3 transformation matrices
            
        Returns:
            3x3 composite transformation matrix
        """
        result = np.eye(3)
        for matrix in matrices:
            result = matrix @ result
        return result


class Visualizer2D:
    """
    A class to visualize 2D shapes and their transformations.
    """
    
    @staticmethod
    def plot_shape(shape, ax, color='blue', label='', alpha=0.7, linestyle='-', linewidth=2):
        """
        Plot a 2D shape on a matplotlib axis.
        
        Args:
            shape: Shape2D object
            ax: Matplotlib axis
            color: Color of the shape
            label: Label for the shape
            alpha: Transparency level
            linestyle: Line style
            linewidth: Line width
        """
        points = shape.current_points
        if shape.name == "Line":
            ax.plot(points[:, 0], points[:, 1], color=color, linewidth=linewidth,
                   linestyle=linestyle, label=label, alpha=alpha)
        else:
            # Close the shape by adding first point at the end
            closed_points = np.vstack([points, points[0]])
            ax.plot(closed_points[:, 0], closed_points[:, 1], color=color,
                   linewidth=linewidth, linestyle=linestyle, label=label, alpha=alpha)
            # Fill the shape
            ax.fill(closed_points[:, 0], closed_points[:, 1], color=color, alpha=alpha*0.3)
    
    @staticmethod
    def plot_comparison(original_shape, transformed_shape, title="", filename=""):
        """
        Plot original and transformed shapes side by side.
        
        Args:
            original_shape: Original Shape2D object
            transformed_shape: Transformed Shape2D object
            title: Title for the plot
            filename: Filename to save the plot (optional)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Save original points to restore later
        original_copy = original_shape.current_points.copy()
        original_shape.current_points = original_shape.original_points.copy()
        
        # Plot original
        Visualizer2D.plot_shape(original_shape, ax1, color='blue', 
                               label='Original', alpha=0.7, linewidth=2)
        ax1.set_title(f'Original {original_shape.name}', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        ax1.legend()
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        
        # Plot transformed
        transformed_shape.current_points = original_copy
        Visualizer2D.plot_shape(transformed_shape, ax2, color='red', 
                               label='Transformed', alpha=0.7, linewidth=2)
        ax2.set_title(f'Transformed {transformed_shape.name}', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        ax2.legend()
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        
        if title:
            fig.suptitle(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()


def create_shapes():
    """Create various 2D shapes for demonstration."""
    # Line
    line = Shape2D([(0, 0), (4, 2)], name="Line")
    
    # Triangle
    triangle = Shape2D([(0, 0), (4, 0), (2, 3)], name="Triangle")
    
    # Rectangle
    rectangle = Shape2D([(0, 0), (4, 0), (4, 3), (0, 3)], name="Rectangle")
    
    # Square
    square = Shape2D([(0, 0), (3, 0), (3, 3), (0, 3)], name="Square")
    
    return {
        'line': line,
        'triangle': triangle,
        'rectangle': rectangle,
        'square': square
    }


def demonstrate_translation():
    """Demonstrate 2D Translation."""
    print("\n" + "="*60)
    print("DEMONSTRATION: 2D TRANSLATION")
    print("="*60)
    
    shapes = create_shapes()
    triangle = shapes['triangle']
    
    print(f"Original Triangle Points:\n{triangle.original_points}\n")
    
    # Apply translation
    trans_matrix = Transformation2D.translation_matrix(tx=5, ty=3)
    print(f"Translation Matrix (tx=5, ty=3):\n{trans_matrix}\n")
    
    triangle.apply_transformation(trans_matrix)
    
    print(f"Transformed Triangle Points:\n{triangle.current_points}\n")
    print("Description: The triangle is moved 5 units right and 3 units up.")
    
    Visualizer2D.plot_comparison(shapes['triangle'], triangle, 
                                title="2D Translation Example")


def demonstrate_rotation():
    """Demonstrate 2D Rotation."""
    print("\n" + "="*60)
    print("DEMONSTRATION: 2D ROTATION")
    print("="*60)
    
    shapes = create_shapes()
    rectangle = shapes['rectangle']
    
    print(f"Original Rectangle Points:\n{rectangle.original_points}\n")
    
    # Apply rotation
    angle = 45  # degrees
    rot_matrix = Transformation2D.rotation_matrix(angle)
    print(f"Rotation Matrix (angle={angle}°):\n{rot_matrix}\n")
    
    rectangle.apply_transformation(rot_matrix)
    
    print(f"Transformed Rectangle Points:\n{rectangle.current_points}\n")
    print(f"Description: The rectangle is rotated {angle}° counter-clockwise about origin.")
    
    Visualizer2D.plot_comparison(shapes['rectangle'], rectangle, 
                                title="2D Rotation Example")


def demonstrate_scaling():
    """Demonstrate 2D Scaling."""
    print("\n" + "="*60)
    print("DEMONSTRATION: 2D SCALING")
    print("="*60)
    
    shapes = create_shapes()
    square = shapes['square']
    
    print(f"Original Square Points:\n{square.original_points}\n")
    
    # Apply scaling
    sx, sy = 2, 1.5
    scale_matrix = Transformation2D.scaling_matrix(sx, sy)
    print(f"Scaling Matrix (sx={sx}, sy={sy}):\n{scale_matrix}\n")
    
    square.apply_transformation(scale_matrix)
    
    print(f"Transformed Square Points:\n{square.current_points}\n")
    print(f"Description: The square is scaled by {sx} in x-axis and {sy} in y-axis.")
    
    Visualizer2D.plot_comparison(shapes['square'], square, 
                                title="2D Scaling Example")


def demonstrate_reflection():
    """Demonstrate 2D Reflection."""
    print("\n" + "="*60)
    print("DEMONSTRATION: 2D REFLECTION")
    print("="*60)
    
    shapes = create_shapes()
    triangle = shapes['triangle']
    
    print(f"Original Triangle Points:\n{triangle.original_points}\n")
    
    # Apply reflection about y-axis
    ref_matrix = Transformation2D.reflection_matrix(axis='y')
    print(f"Reflection Matrix (about Y-axis):\n{ref_matrix}\n")
    
    triangle.apply_transformation(ref_matrix)
    
    print(f"Transformed Triangle Points:\n{triangle.current_points}\n")
    print("Description: The triangle is reflected about the y-axis (mirror image on left).")
    
    Visualizer2D.plot_comparison(shapes['triangle'], triangle, 
                                title="2D Reflection Example (Y-axis)")


def demonstrate_shearing():
    """Demonstrate 2D Shearing."""
    print("\n" + "="*60)
    print("DEMONSTRATION: 2D SHEARING")
    print("="*60)
    
    shapes = create_shapes()
    square = shapes['square']
    
    print(f"Original Square Points:\n{square.original_points}\n")
    
    # Apply shearing
    shx = 0.5  # shearing factor in x-direction
    shy = 0.3  # shearing factor in y-direction
    shear_matrix = Transformation2D.shearing_matrix(shx, shy)
    print(f"Shearing Matrix (shx={shx}, shy={shy}):\n{shear_matrix}\n")
    
    square.apply_transformation(shear_matrix)
    
    print(f"Transformed Square Points:\n{square.current_points}\n")
    print(f"Description: The square is sheared with factors shx={shx} and shy={shy}.")
    
    Visualizer2D.plot_comparison(shapes['square'], square, 
                                title="2D Shearing Example")


def demonstrate_composite_transformations():
    """Demonstrate Composite Transformations."""
    print("\n" + "="*60)
    print("DEMONSTRATION: COMPOSITE TRANSFORMATIONS")
    print("="*60)
    
    shapes = create_shapes()
    
    # Composite Transformation 1: Translation + Rotation + Scaling
    print("\n--- Composite Transformation 1: Translation → Rotation → Scaling ---")
    triangle = shapes['triangle']
    print(f"Original Triangle Points:\n{triangle.original_points}\n")
    
    trans_matrix = Transformation2D.translation_matrix(5, 3)
    rot_matrix = Transformation2D.rotation_matrix(30)
    scale_matrix = Transformation2D.scaling_matrix(1.5, 1.5)
    
    # Combine transformations
    composite_matrix = Transformation2D.composite_transformation(
        scale_matrix, rot_matrix, trans_matrix
    )
    print(f"Composite Matrix:\n{composite_matrix}\n")
    
    triangle.apply_transformation(composite_matrix)
    print(f"Transformed Triangle Points:\n{triangle.current_points}\n")
    print("Description: Triangle is translated, then rotated 30°, then scaled 1.5x")
    
    Visualizer2D.plot_comparison(shapes['triangle'], triangle, 
                                title="Composite Transformation 1: T→R→S")
    
    # Composite Transformation 2: Scaling + Reflection + Translation
    print("\n--- Composite Transformation 2: Scaling → Reflection → Translation ---")
    rectangle = shapes['rectangle']
    rectangle.reset()
    print(f"Original Rectangle Points:\n{rectangle.original_points}\n")
    
    scale_matrix = Transformation2D.scaling_matrix(1.5, 1.5)
    ref_matrix = Transformation2D.reflection_matrix('x')
    trans_matrix = Transformation2D.translation_matrix(3, 4)
    
    composite_matrix = Transformation2D.composite_transformation(
        trans_matrix, ref_matrix, scale_matrix
    )
    print(f"Composite Matrix:\n{composite_matrix}\n")
    
    rectangle.apply_transformation(composite_matrix)
    print(f"Transformed Rectangle Points:\n{rectangle.current_points}\n")
    print("Description: Rectangle is scaled 1.5x, reflected about X-axis, then translated")
    
    Visualizer2D.plot_comparison(shapes['rectangle'], rectangle, 
                                title="Composite Transformation 2: S→Ref→T")
    
    # Composite Transformation 3: Rotation + Shearing + Scaling
    print("\n--- Composite Transformation 3: Rotation → Shearing → Scaling ---")
    square = shapes['square']
    square.reset()
    print(f"Original Square Points:\n{square.original_points}\n")
    
    rot_matrix = Transformation2D.rotation_matrix(20)
    shear_matrix = Transformation2D.shearing_matrix(0.3, 0.2)
    scale_matrix = Transformation2D.scaling_matrix(2, 1.5)
    
    composite_matrix = Transformation2D.composite_transformation(
        scale_matrix, shear_matrix, rot_matrix
    )
    print(f"Composite Matrix:\n{composite_matrix}\n")
    
    square.apply_transformation(composite_matrix)
    print(f"Transformed Square Points:\n{square.current_points}\n")
    print("Description: Square is rotated 20°, sheared, then scaled")
    
    Visualizer2D.plot_comparison(shapes['square'], square, 
                                title="Composite Transformation 3: R→Sh→S")
    
    # Composite Transformation 4: Complex Multi-Transformation
    print("\n--- Composite Transformation 4: T→R→S→Sh→Ref ---")
    line = shapes['line']
    line.reset()
    print(f"Original Line Points:\n{line.original_points}\n")
    
    trans_matrix = Transformation2D.translation_matrix(2, 2)
    rot_matrix = Transformation2D.rotation_matrix(45)
    scale_matrix = Transformation2D.scaling_matrix(2, 2)
    shear_matrix = Transformation2D.shearing_matrix(0.2, 0)
    ref_matrix = Transformation2D.reflection_matrix('y')
    
    composite_matrix = Transformation2D.composite_transformation(
        ref_matrix, shear_matrix, scale_matrix, rot_matrix, trans_matrix
    )
    print(f"Composite Matrix:\n{composite_matrix}\n")
    
    line.apply_transformation(composite_matrix)
    print(f"Transformed Line Points:\n{line.current_points}\n")
    print("Description: Line is translated, rotated, scaled, sheared, and reflected")
    
    Visualizer2D.plot_comparison(shapes['line'], line, 
                                title="Composite Transformation 4: T→R→S→Sh→Ref")


def main():
    """Main function to run all demonstrations."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   2D TRANSFORMATIONS USING HOMOGENEOUS COORDINATES         ║")
    print("║          Computer Graphics Lab Assignment                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Run all demonstrations
    demonstrate_translation()
    demonstrate_rotation()
    demonstrate_scaling()
    demonstrate_reflection()
    demonstrate_shearing()
    demonstrate_composite_transformations()
    
    print("\n" + "="*60)
    print("ALL DEMONSTRATIONS COMPLETED!")
    print("="*60)
    print("\nKey Points:")
    print("✓ All transformations use homogeneous coordinates (x, y, 1)")
    print("✓ All transformation matrices are 3x3")
    print("✓ Composite transformations combine multiple operations")
    print("✓ Matrix order matters in composite transformations")
    print("✓ Visualizations show before and after results")
    print("\n")


if __name__ == "__main__":
    main()
