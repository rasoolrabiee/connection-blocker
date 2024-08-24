import tkinter as tk
from tkinter import filedialog, messagebox
from manage_firewall import manage_firewallclass
import rule_manager
import os
  

file_path_global = None

class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Firewall Manager")
        self.root.geometry("650x400") 
        self.manager = manage_firewallclass()
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)

        
        self.rules_count = 0
        self.rules = rule_manager.load_rules()  # Load rules from file
        
        # Button to select an application
        self.select_button = tk.Button(root, text="Select App", command=self.select_app)
        self.select_button.pack(pady=10)
        
        # Label to display the selected application
        self.path_label = tk.Label(root, text="Select an application")
        self.path_label.pack(pady=5)
        
        # Button to add a firewall rule
        self.add_rule_btn = tk.Button(root, text="Add Rule", command=self.add_rule)
        self.add_rule_btn.pack(pady=5)
        
        # Button to remove a firewall rule
        self.remove_rule_btn = tk.Button(root, text="Remove Rule", command=self.remove_rule)
        self.remove_rule_btn.pack(pady=10)
        
        # Create a canvas and a scrollbar
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        
        # Create a frame to contain the scrollable label
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Configure the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Display existing rules
        self.update_scrollable_frame()

    def select_app(self):
        global file_path_global
        file_path_global = filedialog.askopenfilename()
        if file_path_global:
            self.path_label.config(text=f"Selected application: {file_path_global}")
    
    def add_rule(self):
        if not file_path_global:
            messagebox.showerror("Error", "No application selected")
            return
        
        normalized_path = os.path.normpath(file_path_global)
        rule_name = f"BLOCK_{os.path.basename(normalized_path)}"
        
        result = self.manager.add_firewall_rule(rule_name, normalized_path)
        
        if "Successfully" in result:
            self.rules[rule_name] = normalized_path
            self.rules_count += 1
            
            # Save rules to file
            rule_manager.save_rules(self.rules)
            
            # Add rule to the GUI
            self.add_rule_to_frame(rule_name, normalized_path)
            
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)
        
    def remove_rule(self):
        if not file_path_global:
            messagebox.showerror("Error", "No application selected")
            return
        
        normalized_path = os.path.normpath(file_path_global)
        rule_name = f"BLOCK_{os.path.basename(normalized_path)}"
        
        if rule_name in self.rules:
            result = self.manager.remove_firewall_rule(rule_name)
            if "Successfully" in result:
                del self.rules[rule_name]
                self.rules_count -= 1
                
                # Save rules to file
                rule_manager.save_rules(self.rules)
                
                self.update_scrollable_frame()
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)
        else:
            messagebox.showerror("Error", "Rule not found")
    
    def remove_specific_rule(self, rule_name):
        if rule_name in self.rules:
            result = self.manager.remove_firewall_rule(rule_name)
            if "Successfully" in result:
                del self.rules[rule_name]
                self.rules_count -= 1
                
                # Save rules to file
                rule_manager.save_rules(self.rules)
                
                self.update_scrollable_frame()
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)
    
    def update_scrollable_frame(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        for rule_name, rule_path in self.rules.items():
            self.add_rule_to_frame(rule_name, rule_path)
    
    def add_rule_to_frame(self, rule_name, rule_path):
        rule_frame = tk.Frame(self.scrollable_frame)
        rule_frame.pack(fill="x", pady=2, padx=5)
        
        rule_name_label = tk.Label(rule_frame, text=rule_name, width=30, anchor="w")
        rule_name_label.pack(side="left", padx=5)
        
        rule_path_label = tk.Label(rule_frame, text=rule_path, width=50, anchor="w")
        rule_path_label.pack(side="left", padx=5)
        
        remove_button = tk.Button(rule_frame, text="Remove", command=lambda: self.remove_specific_rule(rule_name))
        remove_button.pack(side="right", padx=5)
        
    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


