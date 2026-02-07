#!/usr/bin/env python3
"""
Timber Frame Designer
Designs timber frame structures based on dimensions and snow load requirements
Includes 3D visualization of the structure
MIT License

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys
import os

class TimberFrameDesigner:
    def __init__(self):
        # Engineering data based on typical timber frame standards
        # Posts: [width, depth] in inches for different load ranges
        self.post_sizes = {
            (0, 30): [6, 6],      # Light snow load
            (30, 50): [8, 8],     # Medium snow load
            (50, 70): [10, 10],   # Heavy snow load
            (70, 100): [12, 12],  # Very heavy snow load
        }
        
        # Beams: [width, depth] in inches based on span and load
        # Format: (span_ft, snow_load_psf): [width, depth]
        self.beam_sizes = {
            # Spans up to 16 feet
            (16, 30): [6, 10],
            (16, 50): [6, 12],
            (16, 70): [8, 12],
            (16, 100): [8, 14],
            # Spans 16-24 feet
            (24, 30): [8, 12],
            (24, 50): [8, 14],
            (24, 70): [10, 14],
            (24, 100): [10, 16],
            # Spans 24-32 feet
            (32, 30): [8, 14],
            (32, 50): [10, 16],
            (32, 70): [12, 16],
            (32, 100): [12, 18],
            # Spans 32-40 feet
            (40, 30): [10, 16],
            (40, 50): [12, 18],
            (40, 70): [12, 20],
            (40, 100): [14, 20],
        }
        
        # Rafters: [width, depth] based on span and load
        self.rafter_sizes = {
            (16, 30): [4, 8],
            (16, 50): [6, 8],
            (16, 70): [6, 10],
            (16, 100): [6, 12],
            (24, 30): [6, 10],
            (24, 50): [6, 12],
            (24, 70): [8, 12],
            (24, 100): [8, 14],
        }
        
    def get_post_size(self, snow_load):
        """Determine post size based on snow load"""
        for (min_load, max_load), size in self.post_sizes.items():
            if min_load <= snow_load < max_load:
                return size
        return [12, 12]  # Default to largest if outside range
    
    def get_beam_size(self, span_ft, snow_load):
        """Determine beam size based on span and snow load"""
        # Find the appropriate size category
        span_categories = [16, 24, 32, 40]
        load_categories = [30, 50, 70, 100]
        
        span_cat = min([s for s in span_categories if span_ft <= s], default=40)
        load_cat = min([l for l in load_categories if snow_load <= l], default=100)
        
        return self.beam_sizes.get((span_cat, load_cat), [12, 18])
    
    def get_rafter_size(self, span_ft, snow_load):
        """Determine rafter size based on span and load"""
        span_categories = [16, 24]
        load_categories = [30, 50, 70, 100]
        
        span_cat = min([s for s in span_categories if span_ft <= s], default=24)
        load_cat = min([l for l in load_categories if snow_load <= l], default=100)
        
        return self.rafter_sizes.get((span_cat, load_cat), [8, 14])

class TimberFrameStructure:
    def __init__(self, length, width, wall_height, roof_pitch, snow_load):
        self.length = length  # feet
        self.width = width    # feet
        self.wall_height = wall_height  # feet
        self.roof_pitch = roof_pitch  # rise/run (e.g., 6/12 = 0.5)
        self.snow_load = snow_load  # psf
        
        self.designer = TimberFrameDesigner()
        self.calculate_dimensions()
        
    def calculate_dimensions(self):
        """Calculate all structural member dimensions"""
        # Post dimensions
        self.post_size = self.designer.get_post_size(self.snow_load)
        
        # Beam dimensions (main beams span the width)
        self.beam_size = self.designer.get_beam_size(self.width, self.snow_load)
        
        # Rafter dimensions
        rafter_span = self.width / 2  # Rafters span from wall to ridge
        self.rafter_size = self.designer.get_rafter_size(rafter_span, self.snow_load)
        
        # Calculate ridge height
        self.ridge_height = self.wall_height + (self.width / 2) * self.roof_pitch
        
        # Bent spacing (typically 8-16 feet on center)
        # Calculate number of bents needed (one at each end, plus intermediate)
        ideal_spacing = 12  # feet - ideal spacing between bents
        self.num_bents = max(2, int(self.length / ideal_spacing) + 1)
        
        # Calculate actual spacing to fit the exact length
        # Space bents evenly across the full length
        self.bent_spacing = self.length / (self.num_bents - 1) if self.num_bents > 1 else self.length
        
    def get_structure_report(self):
        """Generate a detailed structural report"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           TIMBER FRAME STRUCTURE DESIGN REPORT               ║
╚══════════════════════════════════════════════════════════════╝

BUILDING DIMENSIONS:
  Length:        {self.length} ft
  Width:         {self.width} ft
  Wall Height:   {self.wall_height} ft
  Ridge Height:  {self.ridge_height:.1f} ft
  Roof Pitch:    {self.roof_pitch * 12:.0f}/12

DESIGN LOADS:
  Snow Load:     {self.snow_load} psf

STRUCTURAL MEMBERS:
  Posts:         {self.post_size[0]}" × {self.post_size[1]}"
  Beams:         {self.beam_size[0]}" × {self.beam_size[1]}"
  Rafters:       {self.rafter_size[0]}" × {self.rafter_size[1]}"

FRAME LAYOUT:
  Number of Bents: {self.num_bents}
  Bent Spacing:    {self.bent_spacing:.1f} ft on center

MATERIAL REQUIREMENTS (Approximate):
  Posts:         {self.num_bents * 2} pieces @ {self.wall_height} ft
  Beams:         {self.num_bents} pieces @ {self.width} ft
  Rafters:       {self.num_bents * 2} pieces @ {(self.width/2) / np.cos(np.arctan(self.roof_pitch)):.1f} ft
  Plates:        {int(np.ceil(self.length * 2 / 16))} pieces @ 16 ft (both walls)
NOTE: This is a preliminary design. Consult a licensed structural 
engineer for final design and local building code compliance.
        """
        return report
    
    def visualize_3d(self):
        """Create 3D visualization of the timber frame"""
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Convert inches to feet for member dimensions
        post_w = self.post_size[0] / 12
        post_d = self.post_size[1] / 12
        beam_w = self.beam_size[0] / 12
        beam_h = self.beam_size[1] / 12
        rafter_w = self.rafter_size[0] / 12
        rafter_h = self.rafter_size[1] / 12
        
        # Draw each bent
        for i in range(self.num_bents):
            x_pos = i * self.bent_spacing
            
            # Draw 4 corner posts for this bent
            corners = [
                (0, 0), (self.width, 0), (0, self.length), (self.width, self.length)
            ]
            
            # Posts at this bent position
            post_positions = [(0, x_pos), (self.width, x_pos)]
            
            for px, py in post_positions:
                self.draw_post(ax, px, py, 0, self.wall_height, post_w, post_d)
            
            # Draw beams (connecting posts at wall height)
            self.draw_beam(ax, 0, x_pos, self.wall_height, 
                          self.width, x_pos, self.wall_height, beam_w, beam_h)
            
            # Draw rafters
            # Left rafter (from wall to ridge)
            self.draw_rafter(ax, 0, x_pos, self.wall_height,
                           self.width/2, x_pos, self.ridge_height,
                           rafter_w, rafter_h)
            
            # Right rafter (from ridge to wall)
            self.draw_rafter(ax, self.width/2, x_pos, self.ridge_height,
                           self.width, x_pos, self.wall_height,
                           rafter_w, rafter_h)
        
        # Draw connecting plates and purlins
        for i in range(self.num_bents - 1):
            x1 = i * self.bent_spacing
            x2 = (i + 1) * self.bent_spacing
            
            # Wall plates (both sides)
            self.draw_line(ax, 0, x1, self.wall_height, 0, x2, self.wall_height, 'brown', 2)
            self.draw_line(ax, self.width, x1, self.wall_height, 
                          self.width, x2, self.wall_height, 'brown', 2)
            
            # Ridge beam
            self.draw_line(ax, self.width/2, x1, self.ridge_height,
                          self.width/2, x2, self.ridge_height, 'brown', 2)
        
        # Set labels and title
        ax.set_xlabel('Width (ft)', fontsize=10)
        ax.set_ylabel('Length (ft)', fontsize=10)
        ax.set_zlabel('Height (ft)', fontsize=10)
        ax.set_title(f'Timber Frame Structure\n{self.length}ft × {self.width}ft × {self.wall_height}ft walls\nSnow Load: {self.snow_load} psf', 
                     fontsize=12, fontweight='bold')
        
        # Set equal aspect ratio
        max_dim = max(self.length, self.width, self.ridge_height)
        ax.set_xlim([0, max_dim])
        ax.set_ylim([0, max_dim])
        ax.set_zlim([0, max_dim])
        
        # Set viewing angle
        ax.view_init(elev=20, azim=45)
        
        plt.tight_layout()
        return fig
    
    def draw_post(self, ax, x, y, z1, z2, width, depth):
        """Draw a vertical post"""
        # Create vertices for a rectangular post
        vertices = [
            [x - width/2, y - depth/2, z1],
            [x + width/2, y - depth/2, z1],
            [x + width/2, y + depth/2, z1],
            [x - width/2, y + depth/2, z1],
            [x - width/2, y - depth/2, z2],
            [x + width/2, y - depth/2, z2],
            [x + width/2, y + depth/2, z2],
            [x - width/2, y + depth/2, z2],
        ]
        
        # Draw the post as lines
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face
            [4, 5], [5, 6], [6, 7], [7, 4],  # Top face
            [0, 4], [1, 5], [2, 6], [3, 7],  # Vertical edges
        ]
        
        for edge in edges:
            points = [vertices[edge[0]], vertices[edge[1]]]
            ax.plot3D(*zip(*points), 'darkred', linewidth=2)
    
    def draw_beam(self, ax, x1, y1, z1, x2, y2, z2, width, height):
        """Draw a horizontal beam"""
        # Direction vector
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        length = np.sqrt(dx**2 + dy**2 + dz**2)
        
        if length == 0:
            return
        
        # Normalized direction
        dx, dy, dz = dx/length, dy/length, dz/length
        
        # Draw as a thick line (simplified visualization)
        ax.plot3D([x1, x2], [y1, y2], [z1, z2], 'saddlebrown', linewidth=3)
        
        # Draw cross-section at midpoint
        mx, my, mz = (x1 + x2)/2, (y1 + y2)/2, (z1 + z2)/2
        
    def draw_rafter(self, ax, x1, y1, z1, x2, y2, z2, width, height):
        """Draw a rafter"""
        ax.plot3D([x1, x2], [y1, y2], [z1, z2], 'peru', linewidth=3)
    
    def draw_line(self, ax, x1, y1, z1, x2, y2, z2, color, linewidth):
        """Draw a simple line"""
        ax.plot3D([x1, x2], [y1, y2], [z1, z2], color, linewidth=linewidth)

def get_positive_float(prompt, min_val=None, max_val=None):
    """Get a positive float input from user with validation"""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            if min_val is not None and value < min_val:
                print(f"Please enter a value >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Please enter a value <= {max_val}")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         TIMBER FRAME DESIGNER                                ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    print("This program designs timber frame structures based on your")
    print("building dimensions and local snow load requirements.")
    print("\n-Andrew")
    print("andrew@cyberdiary.net")
    print()
    
    # Get building dimensions
    print("BUILDING DIMENSIONS")
    print("-" * 60)
    length = get_positive_float("Enter building length (feet): ", min_val=10, max_val=100)
    width = get_positive_float("Enter building width (feet): ", min_val=10, max_val=60)
    wall_height = get_positive_float("Enter wall height (feet, typical 8-12): ", min_val=6, max_val=20)
    
    print("\nROOF SPECIFICATIONS")
    print("-" * 60)
    print("Common roof pitches: 4/12 (18°), 6/12 (27°), 8/12 (34°), 12/12 (45°)")
    roof_rise = get_positive_float("Enter roof rise (inches per 12 inches run): ", min_val=2, max_val=16)
    roof_pitch = roof_rise / 12
    
    print("\nSNOW LOAD")
    print("-" * 60)
    print("Reference: https://www.ncdc.noaa.gov/snow-and-ice/")
    print("Examples: Southeast 10-20 psf, Midwest 20-40 psf, ")
    print("          Northeast 40-70 psf, Mountain regions 70-150 psf")
    snow_load = get_positive_float("Enter snow load for your area (psf): ", min_val=5, max_val=200)
    
    print("\nCalculating structure...")
    print()
    
    # Create the structure
    structure = TimberFrameStructure(length, width, wall_height, roof_pitch, snow_load)
    
    # Display report
    print(structure.get_structure_report())
    
    # Generate 3D visualization
    print("\nGenerating 3D visualization...")
    fig = structure.visualize_3d()
    
    # Save the figure to current directory
    output_file = "timber_frame_design.png"
    
    try:
        fig.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n3D visualization saved to: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"\nWarning: Could not save image file: {e}")
        print("The 3D visualization will still display in the window.")
    
    # Show interactive plot
    print("\nDisplaying interactive 3D model...")
    print("(Close the window to exit)")
    plt.show()
    
    print("\n✓ Design complete!")
    print("\nREMINDER: This is a preliminary design based on typical timber")
    print("frame construction. Always consult a licensed structural engineer")
    print("and local building codes before construction.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
