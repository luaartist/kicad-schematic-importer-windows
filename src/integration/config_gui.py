import tkinter as tk
from tkinter import ttk
from .auto_config import AutoConfig

class ConfigurationGUI:
    def __init__(self):
        self.config = AutoConfig()
        self.root = tk.Tk()
        self.root.title("KiCad Plugin Manager Configuration")
        
    def show(self):
        """Show configuration GUI"""
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Auto-setup toggle
        ttk.Checkbutton(frame, text="Enable Auto Setup", 
                       variable=tk.BooleanVar(value=self.config.config["auto_setup"])).grid(row=0, column=0)
        
        # Plugin configuration
        for i, (plugin, settings) in enumerate(self.config.config["plugins"].items(), 1):
            ttk.Label(frame, text=plugin).grid(row=i, column=0)
            ttk.Checkbutton(frame, text="Auto Load",
                          variable=tk.BooleanVar(value=settings["auto_load"])).grid(row=i, column=1)
        
        ttk.Button(frame, text="Save", command=self.save_config).grid(row=len(self.config.config["plugins"])+1, column=0)
        
        self.root.mainloop()
        
    def save_config(self):
        """Save configuration and restart manager"""
        self.config.save_config()
        self.root.destroy()