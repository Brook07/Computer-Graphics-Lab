import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

def create_cube():
    """Create vertices for a unit cube"""
    vertices = np.array([
        [-0.5, -0.5, -0.5],  # 0
        [ 0.5, -0.5, -0.5],  # 1
        [ 0.5,  0.5, -0.5],  # 2
        [-0.5,  0.5, -0.5],  # 3
        [-0.5, -0.5,  0.5],  # 4
        [ 0.5, -0.5,  0.5],  # 5
        [ 0.5,  0.5,  0.5],  # 6
        [-0.5,  0.5,  0.5],  # 7
    ])
    
    # Define faces of the cube
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # top
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
        [vertices[4], vertices[7], vertices[3], vertices[0]],  # left
    ]
    
    return vertices, faces

def translation_matrix(tx, ty, tz):
    """Create 4x4 translation matrix"""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def rotation_matrix_x(angle):
    """Create 4x4 rotation matrix about X-axis"""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(angle):
    """Create 4x4 rotation matrix about Y-axis"""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(angle):
    """Create 4x4 rotation matrix about Z-axis"""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def scaling_matrix(sx, sy, sz):
    """Create 4x4 scaling matrix"""
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def shearing_matrix(hxy=0, hxz=0, hyx=0, hyz=0, hzx=0, hzy=0):
    """Create 4x4 shearing matrix"""
    return np.array([
        [1, hyx, hzx, 0],
        [hxy, 1, hzy, 0],
        [hxz, hyz, 1, 0],
        [0, 0, 0, 1]
    ])

def apply_transformation(vertices, matrix):
    """Apply 4x4 transformation matrix to vertices"""
    # Convert to homogeneous coordinates
    ones = np.ones((vertices.shape[0], 1))
    homogeneous_vertices = np.hstack([vertices, ones])
    
    # Apply transformation
    transformed = homogeneous_vertices @ matrix.T
    
    # Convert back to 3D coordinates
    return transformed[:, :3]

def plot_3d_transformation(original_vertices, transformed_vertices, title, filename):
    """Plot original and transformed 3D objects"""
    fig = plt.figure(figsize=(15, 6))
    
    # Original object
    ax1 = fig.add_subplot(121, projection='3d')
    _, faces_orig = create_cube()
    
    # Update faces with original vertices
    faces_orig_updated = []
    for face in faces_orig:
        face_indices = []
        for vertex in face:
            # Find index of this vertex in original_vertices
            for i, orig_vertex in enumerate(original_vertices):
                if np.allclose(vertex, orig_vertex):
                    face_indices.append(i)
                    break
        faces_orig_updated.append([original_vertices[i] for i in face_indices])
    
    poly3d_orig = Poly3DCollection(faces_orig_updated, alpha=0.7, facecolor='lightblue', edgecolor='black')
    ax1.add_collection3d(poly3d_orig)
    
    ax1.scatter(original_vertices[:, 0], original_vertices[:, 1], original_vertices[:, 2], 
                color='red', s=50, alpha=0.8)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Original')
    ax1.set_xlim([-2, 2])
    ax1.set_ylim([-2, 2])
    ax1.set_zlim([-2, 2])
    
    # Transformed object
    ax2 = fig.add_subplot(122, projection='3d')
    
    # Update faces with transformed vertices
    faces_trans_updated = []
    for face in faces_orig:
        face_indices = []
        for vertex in face:
            # Find index of this vertex in original_vertices
            for i, orig_vertex in enumerate(original_vertices):
                if np.allclose(vertex, orig_vertex):
                    face_indices.append(i)
                    break
        faces_trans_updated.append([transformed_vertices[i] for i in face_indices])
    
    poly3d_trans = Poly3DCollection(faces_trans_updated, alpha=0.7, facecolor='lightgreen', edgecolor='black')
    ax2.add_collection3d(poly3d_trans)
    
    ax2.scatter(transformed_vertices[:, 0], transformed_vertices[:, 1], transformed_vertices[:, 2], 
                color='blue', s=50, alpha=0.8)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('Transformed')
    ax2.set_xlim([-3, 3])
    ax2.set_ylim([-3, 3])
    ax2.set_zlim([-3, 3])
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Create fig directory if it doesn't exist
    if not os.path.exists('fig'):
        os.makedirs('fig')
    
    plt.savefig(f'fig/{filename}', dpi=300, bbox_inches='tight')
    plt.show()

def plot_projection_comparison():
    """Compare orthographic and perspective projections"""
    fig = plt.figure(figsize=(15, 6))
    
    # Create multiple cubes at different depths
    vertices, _ = create_cube()
    
    # Orthographic projection (just remove Z coordinate)
    ax1 = fig.add_subplot(121)
    
    depths = [-2, -1, 0, 1, 2]
    colors = ['red', 'orange', 'yellow', 'green', 'blue']
    
    for i, (depth, color) in enumerate(zip(depths, colors)):
        # Translate cube to different depth
        trans_matrix = translation_matrix(0, 0, depth)
        translated_vertices = apply_transformation(vertices, trans_matrix)
        
        # Orthographic projection - just use X,Y coordinates
        ortho_proj = translated_vertices[:, :2]
        
        # Plot the projected vertices
        ax1.scatter(ortho_proj[:, 0], ortho_proj[:, 1], c=color, s=100, alpha=0.7, label=f'Z = {depth}')
        
        # Draw cube outline
        cube_edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # bottom face
            [4, 5], [5, 6], [6, 7], [7, 4],  # top face
            [0, 4], [1, 5], [2, 6], [3, 7]   # vertical edges
        ]
        
        for edge in cube_edges:
            x_coords = [ortho_proj[edge[0], 0], ortho_proj[edge[1], 0]]
            y_coords = [ortho_proj[edge[0], 1], ortho_proj[edge[1], 1]]
            ax1.plot(x_coords, y_coords, color=color, alpha=0.5, linewidth=1)
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title('Orthographic Projection\\n(Size independent of depth)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Perspective projection
    ax2 = fig.add_subplot(122)
    
    # Simple perspective projection: divide by (distance + constant)
    for i, (depth, color) in enumerate(zip(depths, colors)):
        # Translate cube to different depth
        trans_matrix = translation_matrix(0, 0, depth)
        translated_vertices = apply_transformation(vertices, trans_matrix)
        
        # Perspective projection - scale by distance
        distance = 4.0 + translated_vertices[:, 2]  # camera at z=4
        distance = np.maximum(distance, 0.1)  # avoid division by zero
        scale_factor = 2.0 / distance  # perspective scaling
        
        persp_proj = translated_vertices[:, :2] * scale_factor.reshape(-1, 1)
        
        # Plot the projected vertices
        ax2.scatter(persp_proj[:, 0], persp_proj[:, 1], c=color, s=100, alpha=0.7, label=f'Z = {depth}')
        
        # Draw cube outline with perspective
        for edge in cube_edges:
            x_coords = [persp_proj[edge[0], 0], persp_proj[edge[1], 0]]
            y_coords = [persp_proj[edge[0], 1], persp_proj[edge[1], 1]]
            ax2.plot(x_coords, y_coords, color=color, alpha=0.5, linewidth=1)
    
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Perspective Projection\\n(Size decreases with depth)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    plt.suptitle('Orthographic vs Perspective Projection', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if not os.path.exists('fig'):
        os.makedirs('fig')
    
    plt.savefig('fig/projection_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_all_transformations():
    """Generate all transformation visualizations"""
    print("Generating 3D transformation visualizations...")
    
    # Create original cube
    vertices, _ = create_cube()
    
    # 1. Translation Demo
    print("Creating translation demo...")
    trans_matrix = translation_matrix(1.0, 0.5, 0.8)
    transformed_vertices = apply_transformation(vertices, trans_matrix) 
    plot_3d_transformation(vertices, transformed_vertices, 
                          "3D Translation (tx=1.0, ty=0.5, tz=0.8)", 
                          "translation_demo.png")
    
    # 2. Rotation Demo
    print("Creating rotation demo...")
    rot_x = rotation_matrix_x(np.pi/4)
    rot_y = rotation_matrix_y(np.pi/6) 
    rot_z = rotation_matrix_z(np.pi/3)
    combined_rot = rot_z @ rot_y @ rot_x
    transformed_vertices = apply_transformation(vertices, combined_rot)
    plot_3d_transformation(vertices, transformed_vertices,
                          "3D Rotation (rx=45°, ry=30°, rz=60°)",
                          "rotation_demo.png")
    
    # 3. Scaling Demo
    print("Creating scaling demo...")
    scale_matrix = scaling_matrix(1.5, 0.8, 2.0)
    transformed_vertices = apply_transformation(vertices, scale_matrix)
    plot_3d_transformation(vertices, transformed_vertices,
                          "3D Scaling (sx=1.5, sy=0.8, sz=2.0)",
                          "scaling_demo.png")
    
    # 4. Shearing Demo
    print("Creating shearing demo...")
    shear_matrix = shearing_matrix(hxy=0.3, hyz=0.2)
    transformed_vertices = apply_transformation(vertices, shear_matrix)
    plot_3d_transformation(vertices, transformed_vertices,
                          "3D Shearing (hxy=0.3, hyz=0.2)",
                          "shearing_demo.png")
    
    # 5. Combined Transformation
    print("Creating combined transformation demo...")
    combined = (translation_matrix(0.5, 0.3, 0.2) @ 
                rotation_matrix_y(np.pi/4) @ 
                scaling_matrix(1.2, 0.9, 1.1) @
                shearing_matrix(hxy=0.1))
    transformed_vertices = apply_transformation(vertices, combined)
    plot_3d_transformation(vertices, transformed_vertices,
                          "Combined Transformation (T + R + S + H)",
                          "combined_transformation.png")
    
    # 6. Projection Comparison
    print("Creating projection comparison...")
    plot_projection_comparison()
    
    print("All visualizations generated successfully!")

if __name__ == "__main__":
    generate_all_transformations()