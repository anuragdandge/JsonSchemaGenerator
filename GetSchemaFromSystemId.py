
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import requests

# --- UI Constants (for Material-like look) ---
FONT_FAMILY = "Roboto"
FONT_SIZE = 12
PRIMARY_COLOR = "#6200EE"  
TEXT_COLOR = "#212121"  

def extract_terminal_nodes(data):
    """Extracts nodes with empty children along with their paths."""
    terminal_nodes = {}
    stack = [(data, "")]
    while stack:
        item, path = stack.pop()
        if item.get('children') and item['children']:  
            for child in item['children']:
                stack.append((child, f"{path}{item['name']}\\"))
        else:
            full_path = f"{path}{item['name']}"
            terminal_nodes[full_path] = item.get("systemId", None) 
    return terminal_nodes

def on_dropdown_select(event=None):
    """Handles dropdown selection, gets systemId, makes API call, and displays the result."""
    selected_path = dropdown.get()
    system_id = terminal_nodes.get(selected_path, "System ID not found.")

    # Clear previous API response
    api_response_text.delete("1.0", tk.END) 

    if system_id != "System ID not found.":
        response_data = make_api_call(system_id)
        if response_data:
            # Display the API response in the Text widget
            api_response_text.insert(tk.END, json.dumps(response_data, indent=4)) 

def load_json_and_populate_dropdown():
    """Loads JSON from file and populates the dropdown."""
    file_path = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not file_path:
        return  # No file selected

    try:
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        global terminal_nodes
        terminal_nodes = extract_terminal_nodes(json_data)
        node_paths = list(terminal_nodes.keys())

        dropdown['values'] = node_paths
        dropdown.current(0)  
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON data in the file!")

def make_api_call(system_id):
    """Makes the API call with the given systemId and returns the response data."""
    url = 'http://3.210.213.81/Structured_Data/api/ReadCategoryAttributes?_dc=1711015304002'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'insomnia/8.6.1'
    }
    data = {
        'systemId': system_id,
        'filter': 'name,dataTypes'
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status() 
        return response.json()  
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Error making API call:\n{e}")
        return None

# --- Application Setup ---
window = tk.Tk()
window.title("Terminal Node Explorer")
window.configure(bg="#FFFFFF")  

# --- Styles for Material-like UI ---
style = ttk.Style()
style.theme_create("Material", parent="alt", settings={
    "TLabel": {
        "configure": {"font": (FONT_FAMILY, FONT_SIZE), "foreground": TEXT_COLOR}
    },
    "TButton": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE),
            "foreground": "#FFFFFF", 
            "background": PRIMARY_COLOR,
            "borderwidth": 0,
            "padding": 10,
            "relief": "flat"
        },
        "map": {
            "background": [("active", "#536DFE")] 
        }
    },
    "TCombobox": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE), 
            "foreground": TEXT_COLOR,
            "background": "#EEEEEE",
            "arrowsize": 20,        
            "padding": 5 
        }
    }
})
style.theme_use("Material")

# --- Button to Load JSON and Populate Dropdown ---
load_button = ttk.Button(window, text="Load JSON File", command=load_json_and_populate_dropdown)
load_button.pack(pady=20)

# --- Dropdown Setup ---
dropdown_label = ttk.Label(window, text="Select Terminal Node:")
dropdown_label.pack(pady=10)

dropdown = ttk.Combobox(window, values=[], state="readonly", width=40) 
dropdown.pack(pady=10)
dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

# --- Text Widget to Display API Response ---
api_response_label = ttk.Label(window, text="API Response for :")
api_response_label.pack(pady=(20, 5))  # Add padding above the label

api_response_text = tk.Text(window, wrap=tk.WORD, height=10) 
api_response_text.pack(expand=True, fill="both", padx=20, pady=10) 

window.mainloop()