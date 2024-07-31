# JSON Schema Generator and Validator

This Python application provides a graphical user interface (GUI) to generate a JSON Schema from a JSON data file and then validate the generated schema against the original data.

## Features

- **Open JSON File:** Select a JSON file from your system using the file dialog.
- **Schema Generation:** The application automatically generates a JSON Schema based on the structure and data types found in the input JSON file.
- **Schema Validation:**  The generated schema is validated against the original JSON data to ensure correctness.
- **Clear and Concise Output:** The generated schema and validation results are displayed in an easy-to-read format within the application window. 

## Requirements

- **Python 3.x** 
- **Tkinter** (usually included with Python installations)
- **jsonschema** library: Install using `pip install jsonschema`

## How to Use

1. **Save the Code:** Copy the provided Python code and save it as a `.py` file (e.g., `json_schema_app.py`).

2. **Run the Application:**
   - Open your terminal or command prompt.
   - Navigate to the directory where you saved the Python file.
   - Run the script using the command: `python json_schema_app.py`

3. **Using the Application:**
   - A window titled "JSON Schema Generator" will appear.
   - Click the "Open JSON File" button.
   - Select the JSON file you want to use for schema generation.
   - The application will:
     - Load the JSON data from the file.
     - Generate a JSON Schema based on the data.
     - Validate the generated schema against the original data.
   - The generated schema and validation results (success or error message) will be displayed in the application window.

## Code Structure

- **`get_names_with_path(data)` Function:** This function is designed to extract names and paths from hierarchical JSON data. However, it is not directly used in the current version of the application. 

- **`generate_schema()` Function:**
    - Handles file opening using `filedialog`.
    - Reads JSON data using `json.load()`.
    - Generates the JSON Schema by iterating through the `attributes` array in the JSON data:
       - Maps Python data types (`decimal`, `string`, `integer`) to JavaScript data types (`number`, `string`).
       - Adds optional properties like `"description"` and `"enum"` based on specific attribute names. 
    - Performs schema validation using `jsonschema.validate()`.
    - Displays the generated schema and validation results in the Tkinter GUI using a `Text` widget.

- **Tkinter GUI Setup:**
    - Creates the main application window (`tk.Tk()`).
    - Adds a button labeled "Open JSON File" that triggers the `generate_schema()` function.
    - Includes a `Text` widget to display the output.

## Customization

You can customize the schema generation process further:

- **Additional Properties:**  Add more  `if`  conditions within the  `generate_schema()`  function to include other schema properties (e.g., `pattern`, `minLength`, etc.) for specific attributes.
- **Data Type Mapping:** Modify the  `data_type_mapping`  dictionary to handle different data type conversions between Python and JSON Schema.

## Example JSON Input

The application is designed to work with JSON data that has an "attributes" array containing objects with `name`, `dataTypes`, and optional `description` fields.  

## Code 

```python
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
```

## Input :- 
```json
{
  "attributes": [
    {
      "isInherited": "false",
      "systemId": "1ED93D55B6FF48FE853CD9EAAC16BC87",
      "name": "Grip Diameter",
      "description": null,
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "uomType": null,
      "dataTypes": "decimal",
      "allowedValues": null
    },
    {
      "isInherited": "false",
      "systemId": "28E54346EE674901B4504BD0B9EC1247",
      "name": "Grip Length",
      "description": null,
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "uomType": null,
      "dataTypes": "decimal",
      "allowedValues": null
    },
    {
      "isInherited": "false",
      "systemId": "8157A01FED3D416C828AE4F2960F4DA4",
      "name": "Flange Diameter",
      "description": null,
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "uomType": null,
      "dataTypes": "decimal",
      "allowedValues": null
    },
    {
      "isInherited": "false",
      "systemId": "F454EFD932044B66BF0A2881F0E86ABE",
      "name": "Flange thickness",
      "description": null,
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "uomType": null,
      "dataTypes": "decimal",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "289D3DD8FB70409EB56B238AFC2BC86B",
      "name": "Material",
      "description": null,
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": "Steel, 18-8 Stainless, Stainless Steel, Brass, Nylon"
    },
    {
      "isInherited": "true",
      "systemId": "65F7BBCBC2914BE498C1176D00C82322",
      "name": "Thread Pitch",
      "description": "Generally, fastener threads are designed in two ways – as coarse or fine threads. Each design has its own benefits.\r\nMetric thread pitch measurements are read differently than standard ones. While for standard thread pitch measurements the lower number is coarse thread and the higher number refers to fine thread, in metric this is opposite. M10-1.50 is a coarse thread denotation while M10-1.25 is a fine pitch",
      "uniOfMeasure": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "uomType": null,
      "dataTypes": "decimal",
      "allowedValues": ""
    },
    {
      "isInherited": "true",
      "systemId": "6D48CE56E5944DFA8689EE035A4E232A",
      "name": "Dimensional Standards",
      "description": "Dimensional Standards",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "8B4BA3ACBAF740F088A9A29A4ED1C2D9",
      "name": "Head Height",
      "description": "Head Height",
      "uniOfMeasure": "17C6721F68BD4187A1C821BF991A307C ",
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": "17C6721F68BD4187A1C821BF991A307C ",
      "uomType": null,
      "dataTypes": "integer",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "A2B74D8EF6AC4A28B17F5B71D262E1B5",
      "name": "Thread Direction",
      "description": "Right-handed threads have a clockwise direction of torque, while left-handed threads have an anti-clockwise direction of torque. This means that they are designed to resist loosening in different directions.",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": "Right-handed, Left-handed"
    },
    {
      "isInherited": "true",
      "systemId": "CC4BA05AF4B146E593AECB0B54000EAD",
      "name": "Thread Style",
      "description": "Thread Style",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": "Fully Threaded, Partially Threaded"
    },
    {
      "isInherited": "true",
      "systemId": "D4C11232FD6F4E4F8A6131888EA6CE91",
      "name": "Material Grade",
      "description": "The most common class of metric screws and threaded rods. Made of medium-strength steel, ISO Class 8 screws and rods are strong enough for fastening most machinery and equipment. They have a minimum tensile strength of 110,000 psi. Use them with Class 8 or higher nuts.\r\n\r\nISO Class 12.9 fasteners are metric extreme-strength steel screws and threaded rods found in heavy duty equipment, such as bulldozers and excavators. They have a minimum tensile strength of 170,000 psi. Use them with 12 nuts.",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": "Class 8.8, Class 12.9"
    },
    {
      "isInherited": "true",
      "systemId": "DDE9540CE1DF4BF7B1FBFEF84F07880F",
      "name": "Finish",
      "description": "Finish",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "E3665A2955B1482CB9A5A24FEC3E431C",
      "name": "Fastener Standard",
      "description": "Fastener Standards",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "E62220879E574D02B0225618C17AD0AD",
      "name": "Fastener Length",
      "description": null,
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "decimal",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "E7F7CDE4526145E0BF56B35242DBD421",
      "name": "Minimum Thread Length",
      "description": "Minimum Thread Length",
      "uniOfMeasure": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": "994CBC57C3B24AC19A6F01A49C181F14 ",
      "uomType": null,
      "dataTypes": "integer",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "EBCAF16919B448AFBA6EDE53716A59B9",
      "name": "Material Standards",
      "description": "Material specification means a document detailing the list of tests, formulations, references to any analytical methods and appropriate acceptance criteria that are numerical limits, ranges or other criteria for tests described, that establishes a set of criteria to which any Product Material should conform to be .",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": "Steel, 18-8 Stainless, Stainless Steel, Brass, Nylon"
    },
    {
      "isInherited": "true",
      "systemId": "FBA702CD130C41EE8CA90958183FA130",
      "name": "Tensile Strength",
      "description": "Tensile strength can be defined as the maximum stress that a material can bear before breaking when it is allowed to be stretched or pulled.",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "integer",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "5669D879353F4A128092E2EE6A073653",
      "name": "Legacy Part Number",
      "description": "Legacy Part Number and defined from customer.",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "item",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "AA6CE0579DC54A38BAAAF97C980DD1CC",
      "name": "Noun",
      "description": "Noun",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": null
    },
    {
      "isInherited": "true",
      "systemId": "F4AEB9ABF87D4E67AD86206757F56243",
      "name": "Legacy Description",
      "description": "Legacy Description as provided by customer",
      "uniOfMeasure": null,
      "inRange": "0",
      "rangeMin": null,
      "rangeMax": null,
      "attributeGroup": null,
      "uom": null,
      "uomType": null,
      "dataTypes": "string",
      "allowedValues": null
    }
  ]
}
```

## Output :-

```json
{
    "type": "object",
    "properties": {
        "Grip Diameter": {
            "type": "number"
        },
        "Grip Length": {
            "type": "number"
        },
        "Flange Diameter": {
            "type": "number"
        },
        "Flange thickness": {
            "type": "number"
        },
        "Material": {
            "type": "string",
            "enum": [
                "Steel",
                "18-8 Stainless",
                "Stainless Steel",
                "Brass",
                "Nylon"
            ]
        },
        "Thread Pitch": {
            "type": "number",
            "description": "Generally, fastener threads are designed in two ways \u00e2\u20ac\u201c as coarse or fine threads. Each design has its own benefits.\r\nMetric thread pitch measurements are read differently than standard ones. While for standard thread pitch measurements the lower number is coarse thread and the higher number refers to fine thread, in metric this is opposite. M10-1.50 is a coarse thread denotation while M10-1.25 is a fine pitch"
        },
        "Dimensional Standards": {
            "type": "string",
            "description": "Dimensional Standards"
        },
        "Head Height": {
            "type": "number",
            "description": "Head Height"
        },
        "Thread Direction": {
            "type": "string",
            "description": "Right-handed threads have a clockwise direction of torque, while left-handed threads have an anti-clockwise direction of torque. This means that they are designed to resist loosening in different directions."
        },
        "Thread Style": {
            "type": "string",
            "description": "Thread Style"
        },
        "Material Grade": {
            "type": "string",
            "description": "The most common class of metric screws and threaded rods. Made of medium-strength steel, ISO Class 8 screws and rods are strong enough for fastening most machinery and equipment. They have a minimum tensile strength of 110,000 psi. Use them with Class 8 or higher nuts.\r\n\r\nISO Class 12.9 fasteners are metric extreme-strength steel screws and threaded rods found in heavy duty equipment, such as bulldozers and excavators. They have a minimum tensile strength of 170,000 psi. Use them with 12 nuts."
        },
        "Finish": {
            "type": "string",
            "description": "Finish"
        },
        "Fastener Standard": {
            "type": "string",
            "description": "Fastener Standards"
        },
        "Fastener Length": {
            "type": "number"
        },
        "Minimum Thread Length": {
            "type": "number",
            "description": "Minimum Thread Length"
        },
        "Material Standards": {
            "type": "string",
            "description": "Material specification means a document detailing the list of tests, formulations, references to any analytical methods and appropriate acceptance criteria that are numerical limits, ranges or other criteria for tests described, that establishes a set of criteria to which any Product Material should conform to be ."
        },
        "Tensile Strength": {
            "type": "number",
            "description": "Tensile strength can be defined as the maximum stress that a material can bear before breaking when it is allowed to be stretched or pulled."
        },
        "Legacy Part Number": {
            "type": "string",
            "description": "Legacy Part Number and defined from customer."
        },
        "Noun": {
            "type": "string",
            "description": "Noun"
        },
        "Legacy Description": {
            "type": "string",
            "description": "Legacy Description as provided by customer"
        }
    }
}

JSON Schema is valid.

```
