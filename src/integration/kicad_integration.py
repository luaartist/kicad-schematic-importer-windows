from .kicad_python_wrapper import KicadPythonWrapper
import os
import cv2
import numpy as np
from skidl import *

class KiCadSchematicGenerator:
    def __init__(self, output_dir="kicad_output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Initialize KiCad integration
        self.kicad = KicadPythonWrapper()
        
        # Check KiCad version and initialize modules
        print(f"KiCad Version: {self.kicad.kicad_version}")
        print(f"KiCad 9+ Compatible: {self.kicad.is_kicad9}")
        
        modules = self.kicad.import_kicad_modules()
        self.pcbnew = modules.get('pcbnew')
        
        if not self.pcbnew:
            raise ImportError("Failed to initialize KiCad integration")

    def load_project(self, project_path: str) -> bool:
        """Load and synchronize with a KiCad project"""
        if not self.kicad.sync_project(project_path):
            print("Failed to synchronize with KiCad project")
            return False
        
        self.board = self.kicad.get_board()
        return True

    def detect_components_from_image(self, image_path):
        """Detect components from schematic image and create KiCad components"""
        print(f"Processing image: {image_path}")
        
        # Load and process image with OpenCV
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert to grayscale and apply preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 100, 200)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size
        min_area = 100
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        # Process each detected component
        components = []
        for i, contour in enumerate(filtered_contours):
            x, y, w, h = cv2.boundingRect(contour)
            
            # Classify component type based on shape/size
            component_type = self._classify_component(contour, w, h)
            
            # Create component in KiCad
            component = self._create_kicad_component(component_type, i, x, y)
            components.append(component)
            
            # Draw on image for visualization
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, f"{component_type} {i}", (x, y-5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Save visualization
        cv2.imwrite(os.path.join(self.output_dir, "detected_components.png"), image)
        
        return components
    
    def _classify_component(self, contour, width, height):
        """Classify component type based on shape and size"""
        aspect_ratio = float(width) / height if height > 0 else 0
        area = cv2.contourArea(contour)
        
        # Simple classification rules (can be enhanced with ML)
        if aspect_ratio > 2.5:
            return 'resistor'
        elif 0.8 < aspect_ratio < 1.2 and area < 5000:
            return 'capacitor'
        elif area > 10000:
            return 'ic'
        else:
            return 'connector'
    
    def _create_kicad_component(self, component_type, index, x, y):
        """Create a KiCad component based on detected type"""
        # Get template for this component type
        template = self.component_templates.get(component_type, self.component_templates['resistor'])
        
        # Create module (footprint)
        module = pcbnew.FootprintLoad(
            pcbnew.FOOTPRINT_LIBRARY_PATHS[0],  # Use first available library path
            template['footprint'].split(':')[1]  # Extract footprint name without library prefix
        )
        
        if module is None:
            print(f"Warning: Could not load footprint {template['footprint']}")
            # Create a default module as fallback
            module = pcbnew.FOOTPRINT(self.board)
            module.SetReference(f"{component_type.upper()[0]}{index}")
        else:
            module.SetReference(f"{component_type.upper()[0]}{index}")
        
        # Set position (convert from pixel coordinates to KiCad units)
        # KiCad uses nanometers as internal units
        scale_factor = 10000  # Adjust based on your image scale
        position = pcbnew.VECTOR2I(int(x * scale_factor), int(y * scale_factor))
        module.SetPosition(position)
        
        # Add to board
        self.board.Add(module)
        
        return {
            'type': component_type,
            'id': index,
            'module': module,
            'position': (x, y)
        }
    
    def detect_connections(self, image_path):
        """Detect connections between components"""
        # Load image
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use HoughLinesP to detect lines (potential connections)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)
        
        connections = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Find components near line endpoints
                start_component = self._find_component_at_position(x1, y1)
                end_component = self._find_component_at_position(x2, y2)
                
                if start_component and end_component and start_component != end_component:
                    connections.append((start_component, end_component))
                    
                    # Create track in KiCad
                    track = pcbnew.PCB_TRACK(self.board)
                    scale_factor = 10000  # Same scale as used for components
                    track.SetStart(pcbnew.VECTOR2I(int(x1 * scale_factor), int(y1 * scale_factor)))
                    track.SetEnd(pcbnew.VECTOR2I(int(x2 * scale_factor), int(y2 * scale_factor)))
                    track.SetWidth(pcbnew.FromMM(0.2))  # 0.2mm track width
                    self.board.Add(track)
        
        return connections
    
    def _find_component_at_position(self, x, y, tolerance=20):
        """Find component near given position"""
        # This would need to be implemented based on your component storage
        # For now, return a placeholder
        return None
    
    def generate_netlist_with_skidl(self, components, connections):
        """Generate netlist using SKiDL"""
        # Start a new circuit
        reset()
        
        # Create components in SKiDL
        skidl_components = {}
        for comp in components:
            if comp['type'] == 'resistor':
                skidl_components[comp['id']] = Part('Device', 'R', value='10K', footprint=self.component_templates['resistor']['footprint'])
            elif comp['type'] == 'capacitor':
                skidl_components[comp['id']] = Part('Device', 'C', value='0.1uF', footprint=self.component_templates['capacitor']['footprint'])
            elif comp['type'] == 'ic':
                skidl_components[comp['id']] = Part('Amplifier_Operational', 'LM358', footprint=self.component_templates['ic']['footprint'])
            else:
                skidl_components[comp['id']] = Part('Connector', 'Conn_01x04_Male', footprint=self.component_templates['connector']['footprint'])
        
        # Create connections
        for start_comp, end_comp in connections:
            if start_comp['id'] in skidl_components and end_comp['id'] in skidl_components:
                # Connect first pins as a simple example
                # In a real implementation, you'd need to determine which pins to connect
                skidl_components[start_comp['id']][1] += skidl_components[end_comp['id']][1]
        
        # Generate netlist
        netlist_path = os.path.join(self.output_dir, "generated_netlist.net")
        generate_netlist(netlist_path)
        
        return netlist_path
    
    def save_kicad_project(self):
        """Save the KiCad project files"""
        # Save board file
        board_path = os.path.join(self.output_dir, "generated_board.kicad_pcb")
        pcbnew.SaveBoard(board_path, self.board)
        
        print(f"KiCad board saved to: {board_path}")
        
        # If we had a schematic, we would save it here
        
        return board_path

def main():
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Process schematic image and create KiCad project')
    parser.add_argument('--image', type=str, required=True, help='Path to schematic image')
    parser.add_argument('--output', type=str, default='kicad_output', help='Output directory')
    parser.add_argument('--project', type=str, help='Path to existing KiCad project (optional)')
    args = parser.parse_args()
    
    try:
        # Initialize KiCad generator
        generator = KiCadSchematicGenerator(args.output)
        
        # Load existing project if specified
        if args.project:
            print("Loading KiCad project...")
            if generator.load_project(args.project):
                print("Successfully synchronized with KiCad project")
            else:
                print("Failed to load KiCad project")
                return
        
        # Detect components
        print("Detecting components...")
        components = generator.detect_components_from_image(args.image)
        print(f"Detected {len(components)} components")
        
        # Detect connections
        print("Detecting connections...")
        connections = generator.detect_connections(args.image)
        print(f"Detected {len(connections)} connections")
        
        # Generate netlist
        print("Generating netlist...")
        netlist_path = generator.generate_netlist_with_skidl(components, connections)
        print(f"Netlist generated: {netlist_path}")
        
        # Save KiCad project
        print("Saving KiCad project...")
        board_path = generator.save_kicad_project()
        
        print("Process completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
