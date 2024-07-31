import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# --- UI Constants (for Material-like look) ---
FONT_FAMILY = "Roboto"  # Or any other modern font you prefer
FONT_SIZE = 12
PRIMARY_COLOR = "#6200EE"  # Example primary color (purple)
TEXT_COLOR = "#212121"  # Dark grey for text

def extract_terminal_nodes(data):
    """Extracts nodes with empty children along with their paths."""
    terminal_nodes = {}
    stack = [(data, "")]
    while stack:
        item, path = stack.pop()
        if item.get('children') and item['children']:  # Only process non-empty children
            for child in item['children']:
                stack.append((child, f"{path}{item['name']}\\"))
        else:
            full_path = f"{path}{item['name']}"
            terminal_nodes[full_path] = item.get("systemId", None) # Store systemId
    return terminal_nodes

def on_dropdown_select(event=None):
    """Handles dropdown selection and displays systemId."""
    selected_path = dropdown.get()
    system_id = terminal_nodes.get(selected_path, "System ID not found.")
    messagebox.showinfo("System ID", f"System ID for '{selected_path}':\n{system_id}")

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
        dropdown.current(0)  # Select the first item by default
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON data in the file!")

# --- Application Setup ---
window = tk.Tk()
window.title("Terminal Node Explorer")
window.configure(bg="#FFFFFF") # Set background to white

# --- Styles for Material-like UI ---
style = ttk.Style()
style.theme_create("Material", parent="alt", settings={
    "TLabel": {
        "configure": {"font": (FONT_FAMILY, FONT_SIZE), "foreground": TEXT_COLOR}
    },
    "TButton": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE),
            "foreground": "#FFFFFF",  # White text on buttons
            "background": PRIMARY_COLOR,
            "borderwidth": 0,
            "padding": 10,
            "relief": "flat"
        },
        "map": {
            "background": [("active", "#536DFE")] # Darker shade on click
        }
    },
    "TCombobox": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE), 
            "foreground": TEXT_COLOR,
            "background": "#EEEEEE", # Light grey background for combobox
            "arrowsize": 20,        # Larger arrow
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

dropdown = ttk.Combobox(window, values=[], state="readonly", width=40)  # Set width here
dropdown.pack(pady=10)
dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

window.mainloop()