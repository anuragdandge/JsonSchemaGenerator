import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Text
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import requests
import time

# --- UI Constants (for Material-like look) ---
FONT_FAMILY = "Roboto"
FONT_SIZE = 12
PRIMARY_COLOR = "#6200EE"
TEXT_COLOR = "#212121"

# --- Global variables ---
terminal_nodes = {}
api_response_data = None
category_items_data = None

# --- Functions ---
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
    """Handles dropdown selection, gets systemId, makes API calls, 
       stores responses, and displays them."""
    global api_response_data, category_items_data
    selected_path = dropdown.get()
    system_id = terminal_nodes.get(selected_path, "System ID not found.")

    # Clear previous API responses
    api_response_text.delete("1.0", tk.END)
    category_items_text.delete("1.0", tk.END)

    if system_id != "System ID not found.":
        # Make API calls
        start_loading_animation()
        api_response_data = make_api_call(system_id, 
                                    'http://3.210.213.81/Structured_Data/api/ReadCategoryAttributes?_dc=1711015759216')
        if api_response_data:
            api_response_text.insert(tk.END, json.dumps(api_response_data, indent=4))
            
        category_items_data = make_api_call(system_id, 
                                        'http://3.210.213.81/Structured_Data/api/ReadCategoryItems?_dc=1711015759216')
        if category_items_data:
            clean_and_display_items_data(category_items_data)  # Clean and display

        stop_loading_animation()
        generate_schema_button.config(state=tk.NORMAL) 

def load_json_and_populate_dropdown():
    """Loads JSON from file and populates the dropdown."""
    global terminal_nodes
    file_path = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not file_path:
        return  # No file selected

    try:
        start_loading_animation()
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        terminal_nodes = extract_terminal_nodes(json_data)
        node_paths = list(terminal_nodes.keys())

        dropdown['values'] = node_paths
        dropdown.current(0)
        stop_loading_animation()

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON data in the file!")

def make_api_call(system_id, url):
    """Makes the API call with the given systemId and URL."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'insomnia/8.6.1'
    }
    data = {
        'systemId': system_id
        # Add other parameters if needed based on the API
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Error making API call to {url}:\n{e}")
        return None

def generate_schema():
    """Generates JSON schema from the first API response data."""
    global api_response_data
    try:
        if api_response_data is None:
            messagebox.showwarning("Make API Call First", 
                                   "Please select a terminal node and make an API call to get data for schema generation.")
            return

        start_loading_animation()
        schema_text.delete("1.0", tk.END)

        schema_properties = {}
        for item in api_response_data.get('attributes', []):
            name = item.get('name')
            data_type = item.get('dataTypes')

            if not name or not data_type:
                messagebox.showwarning("Data Warning", "Skipping item due to missing 'name' or 'dataTypes'")
                continue

            data_type_mapping = {
                "decimal": "number",
                "string": "string",
                "integer": "number",
                "item": "string"
            }
            js_data_type = data_type_mapping.get(data_type, data_type)
            property_schema = {"type": js_data_type}

            if item.get('description'):
                property_schema["description"] = item['description']

            if name == "Material":
                property_schema["enum"] = ["Steel", "18-8 Stainless", "Stainless Steel", "Brass", "Nylon"]

            schema_properties[name] = property_schema

        schema = {
            "type": "object",
            "properties": schema_properties
        }

        try:
            validate(instance=api_response_data, schema=schema)
            validation_result = "JSON Schema is valid."
        except ValidationError as e:
            validation_result = f"JSON Schema Validation Error:\n{e}"

        schema_text.insert(tk.END, json.dumps(schema, indent=4) + "\n\n")
        schema_text.insert(tk.END, validation_result)
        stop_loading_animation()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during schema generation:\n{e}")

# --- Loading Animation Functions ---
def start_loading_animation():
    """Starts the loading animation."""
    global loading_label
    loading_label = ttk.Label(window, text="Processing...", font=(FONT_FAMILY, FONT_SIZE))
    loading_label.pack(pady=10)
    window.update() 

def stop_loading_animation():
    """Stops the loading animation."""
    global loading_label
    if loading_label:
        loading_label.destroy()
        window.update() 

def clean_and_display_items_data(data):
    """Cleans the response from the second API call 
       and displays the cleaned data."""
    try:
        if data and "attributes" in data and len(data["attributes"]) > 0:
            items_data_str = data["attributes"][0]  # Get the string from the list
            items_data = json.loads(items_data_str)  # Parse the string as JSON
            cleaned_items_data = items_data.get("ItemsData", [])
            category_items_text.delete("1.0", tk.END)
            category_items_text.insert(tk.END, json.dumps(cleaned_items_data, indent=4))
        else:
            category_items_text.delete("1.0", tk.END)
            category_items_text.insert(tk.END, "No valid items data found in the response.")

    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Error parsing API response:\n{e}")
        return None

# --- Application Setup ---
window = tk.Tk()
window.title("Terminal Node Explorer & Schema Generator")
window.configure(bg="#FFFFFF")

# --- Styles for Material-like UI ---
# ... (same as before) 

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


# --- Layout ---
# Top Frame for file loading and dropdown
top_frame = tk.Frame(window, bg="#FFFFFF")
top_frame.pack(pady=20)

load_button = ttk.Button(top_frame, text="Load JSON File", 
                        command=load_json_and_populate_dropdown)
load_button.pack(side=tk.LEFT, padx=(0, 10))

dropdown_label = ttk.Label(top_frame, text="Select Terminal Node:")
dropdown_label.pack(side=tk.LEFT)

dropdown = ttk.Combobox(top_frame, values=[], state="readonly", width=40)
dropdown.pack(side=tk.LEFT, padx=(10, 0))
dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

# Bottom Frame for API responses and schema
bottom_frame = tk.Frame(window, bg="#FFFFFF")
bottom_frame.pack(pady=10, expand=True, fill="both")

# API Responses Section
api_responses_frame = tk.Frame(bottom_frame, bg="#FFFFFF")
api_responses_frame.pack(side=tk.LEFT, padx=20, pady=(0, 10), fill=tk.BOTH, expand=True)

# First API Response
api_response_label = ttk.Label(api_responses_frame, text="API Response 1:")
api_response_label.pack(pady=(0, 5), anchor='w')
api_response_text = Text(api_responses_frame, wrap=tk.WORD, height=10)
api_response_text.pack(expand=True, fill="both")

# Second API Response
category_items_label = ttk.Label(api_responses_frame, text="API Response 2:")
category_items_label.pack(pady=(10, 5), anchor='w')
category_items_text = Text(api_responses_frame, wrap=tk.WORD, height=10)
category_items_text.pack(expand=True, fill="both")

# Schema Generation and Display Section
schema_frame = tk.Frame(bottom_frame, bg="#FFFFFF")
schema_frame.pack(side=tk.LEFT, padx=(0, 20), pady=(0, 10), fill=tk.BOTH, expand=True)

generate_schema_button = ttk.Button(
    schema_frame, text="Generate JSON Schema", command=generate_schema, state=tk.DISABLED
)
generate_schema_button.pack(pady=(0, 10))
schema_text = Text(schema_frame, wrap=tk.WORD)
schema_text.pack(expand=True, fill="both")

# Configure weights to allow resizing
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)

window.mainloop()