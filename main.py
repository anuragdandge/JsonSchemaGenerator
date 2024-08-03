# import tkinter as tk
# from tkinter import messagebox, scrolledtext
# import json
# import jsonschema
# from genson import SchemaBuilder

# # Function to generate JSON schema
# def generate_schema(json_data):
#     try:
#         data = json.loads(json_data)
#         builder = SchemaBuilder()
#         builder.add_object(data)
#         schema = builder.to_schema()
#         return schema
#     except json.JSONDecodeError as e:
#         messagebox.showerror("Error", f"Invalid JSON: {e}")
#     except Exception as e:
#         messagebox.showerror("Error", f"Schema generation failed: {e}")
#     return None

# # Function to validate JSON against schema
# def validate_json(json_data, schema):
#     try:
#         data = json.loads(json_data)
#         validator = jsonschema.Draft7Validator(schema)
#         errors = list(validator.iter_errors(data))
#         if errors:
#             error_messages = "\n".join(str(e.message) for e in errors)
#             messagebox.showerror("Validation Errors", error_messages)
#         else:
#             messagebox.showinfo("Success", "JSON is valid!")
#     except json.JSONDecodeError as e:
#         messagebox.showerror("Error", f"Invalid JSON: {e}")
#     except Exception as e:
#         messagebox.showerror("Error", f"Validation failed: {e}")

# # Function to handle the Generate Schema button
# def on_generate_schema():
#     json_data = json_input.get("1.0", tk.END).strip()
#     schema = generate_schema(json_data)
#     if schema:
#         schema_output.delete("1.0", tk.END)
#         schema_output.insert(tk.END, json.dumps(schema, indent=4))

# # Function to handle the Validate JSON button
# def on_validate_json():
#     json_data = json_input.get("1.0", tk.END).strip()
#     schema = schema_output.get("1.0", tk.END).strip()
#     try:
#         schema = json.loads(schema)
#         validate_json(json_data, schema)
#     except json.JSONDecodeError as e:
#         messagebox.showerror("Error", f"Invalid Schema: {e}")

# # Main window setup
# root = tk.Tk()
# root.title("JSON Schema Generator")

# # Input JSON text area
# tk.Label(root, text="Input JSON:").pack()
# json_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
# json_input.pack()

# # Buttons
# tk.Button(root, text="Generate Schema", command=on_generate_schema).pack()
# tk.Button(root, text="Validate JSON", command=on_validate_json).pack()

# # Output schema text area
# tk.Label(root, text="Generated Schema:").pack()
# schema_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
# schema_output.pack()

# # Run the application
# root.mainloop()

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



# import json
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog

# def extract_terminal_nodes(data):
#     """Extracts nodes with empty children along with their paths."""
#     terminal_nodes = {}
#     stack = [(data, "")]
#     while stack:
#         item, path = stack.pop()
#         if item.get('children') and item['children']:  # Only process non-empty children
#             for child in item['children']:
#                 stack.append((child, f"{path}{item['name']}\\"))
#         else:
#             full_path = f"{path}{item['name']}"
#             terminal_nodes[full_path] = item.get("systemId", None) # Store systemId
#     return terminal_nodes

# def on_dropdown_select(event=None):
#     """Handles dropdown selection and displays systemId."""
#     selected_path = dropdown.get()
#     system_id = terminal_nodes.get(selected_path, "System ID not found.")
#     messagebox.showinfo("System ID", f"System ID for '{selected_path}':\n{system_id}")

# def load_json_and_populate_dropdown():
#     """Loads JSON from file and populates the dropdown."""
#     file_path = filedialog.askopenfilename(
#         defaultextension=".json",
#         filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
#     )
#     if not file_path:
#         return  # No file selected

#     try:
#         with open(file_path, 'r') as f:
#             json_data = json.load(f)

#         global terminal_nodes
#         terminal_nodes = extract_terminal_nodes(json_data)
#         node_paths = list(terminal_nodes.keys())

#         dropdown['values'] = node_paths
#         dropdown.current(0)  # Select the first item by default
#     except FileNotFoundError:
#         messagebox.showerror("Error", "File not found!")
#     except json.JSONDecodeError:
#         messagebox.showerror("Error", "Invalid JSON data in the file!")

# # --- Application Setup ---
# window = tk.Tk()
# window.title("Terminal Node Explorer")

# # --- Button to Load JSON and Populate Dropdown ---
# load_button = tk.Button(window, text="Load JSON File", command=load_json_and_populate_dropdown)
# load_button.pack(pady=10)

# # --- Dropdown Setup ---
# dropdown_label = tk.Label(window, text="Select Terminal Node:")
# dropdown_label.pack(pady=10)

# dropdown = ttk.Combobox(window, values=[], state="readonly")  # Initially empty
# dropdown.pack(pady=10)
# dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)  # Bind selection event

# window.mainloop()