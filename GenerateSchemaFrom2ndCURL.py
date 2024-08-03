
import json
import tkinter as tk
from tkinter import filedialog, messagebox, Text
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def get_names_with_path(data):
    """Extracts names from a hierarchical JSON structure, building paths for
    items with children. Ignores the root element if its name is '.'.

    Args:
        data: The hierarchical JSON data.

    Returns:
        A list of names with paths.
    """
    names_with_path = []
    stack = [(data, "")]  # Start with the root and an empty path

    while stack:
        item, path = stack.pop()

        # Skip if it's the root element with name "."
        if path == "" and item.get('name') == '.':
            if item.get('children'):
                for child in item['children']:
                    stack.append((child, path))
            continue

        current_name = f"{path}{item['name']}"

        if item.get('children'):
            # If the item has children, add its path
            names_with_path.append(current_name)
            # Add children to the stack for processing with the updated path
            for child in item['children']:
                stack.append((child, current_name + "\\"))
        else:
            # If no children, just add the name
            names_with_path.append(current_name)

    return names_with_path


def generate_schema():
    """Generates the JSON schema from the loaded JSON data."""
    try:
        # Clear output text box
        output_text.delete("1.0", tk.END)

        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return  # No file selected

        with open(file_path, 'r') as f:
            json_data = json.load(f)

        schema_properties = {}
        for attr in json_data.get('attributes', []):
            name = attr['name']
            data_type = attr['dataTypes']

            # Map Python data types to JavaScript data types
            data_type_mapping = {
                "decimal": "number",
                "string": "string",
                "integer": "number",
                "item": "string"
            }
            js_data_type = data_type_mapping.get(data_type, data_type)

            # Create property schema
            property_schema = {"type": js_data_type}

            # Add description if available
            if attr['description']:
                property_schema["description"] = attr['description']

            # --- Additional Properties (Modify as needed) ---
            if name == "Material":  
                property_schema["enum"] = ["Steel", "18-8 Stainless", "Stainless Steel", "Brass", "Nylon"]

            # Add more conditions and properties as needed...

            # Assign the property schema
            schema_properties[name] = property_schema

        schema = {
            "type": "object",
            "properties": schema_properties
        }

        # --- Schema Validation ---
        try:
            validate(instance=json_data, schema=schema)
            validation_result = "JSON Schema is valid."
        except ValidationError as e:
            validation_result = f"JSON Schema Validation Error:\n{e}"

        # --- Display Results ---
        output_text.insert(tk.END, json.dumps(schema, indent=4) + "\n\n")
        output_text.insert(tk.END, validation_result)

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON data in the file!")

# --- Tkinter GUI Setup ---
window = tk.Tk()
window.title("JSON Schema Generator")

# Button to open file dialog
open_button = tk.Button(window, text="Open JSON File", command=generate_schema)
open_button.pack(pady=20)

# Output text box
output_text = Text(window, wrap=tk.WORD)
output_text.pack(expand=True, fill="both", padx=20, pady=20)

window.mainloop()

