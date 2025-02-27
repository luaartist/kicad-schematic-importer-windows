class StackupManager:
    def __init__(self):
        self.current_stackup = None
        self.templates = self.load_stackup_templates()
        
    def apply_stackup_template(self, template_name: str):
        """Apply a predefined stackup template"""
        template = self.templates.get(template_name)
        if template:
            self.current_stackup = template.copy()
            return self.update_layout_rules()
            
    def create_custom_stackup(self, layers: List[Dict]):
        """Create custom stackup configuration"""
        self.current_stackup = {
            'layers': layers,
            'rules': self.generate_stackup_rules(layers)
        }
        return self.update_layout_rules()
        
    def generate_stackup_rules(self, layers):
        """Generate DRC rules for stackup"""
        return {
            'min_trace_width': self.calculate_min_trace_width(layers),
            'min_spacing': self.calculate_min_spacing(layers),
            'via_rules': self.generate_via_rules(layers)
        }