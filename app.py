# import json

# def get_names_with_path(data):
#   """Extracts names from a hierarchical JSON structure, building paths for 
#   items with children. Ignores the root element if its name is '.'.

#   Args:
#     data: The hierarchical JSON data.

#   Returns:
#     A list of names with paths.
#   """

#   names_with_path = []
#   stack = [(data, "")]  # Start with the root and an empty path

#   while stack:
#     item, path = stack.pop()

#     # Skip if it's the root element with name "."
#     if path == "" and item.get('name') == '.': 
#       if item.get('children'):
#         for child in item['children']:
#           stack.append((child, path)) 
#       continue 

#     current_name = f"{path}{item['name']}"

#     if item.get('children'):
#       # If the item has children, add its path
#       names_with_path.append(current_name)
#       # Add children to the stack for processing with the updated path
#       for child in item['children']:
#         stack.append((child, current_name + "\\"))
#     else:
#       # If no children, just add the name
#       names_with_path.append(current_name) 

#   return names_with_path

# # --- Dynamic Input ---
# # 1. From a JSON file:
# file_path = input("Enter the path to your JSON file: ") 
# with open(file_path, 'r') as f:
#   json_data = json.load(f)

# # 2. Or, directly from user input as a string:
# # json_string = input("Enter your JSON data: ")
# # json_data = json.loads(json_string)

# # --- Process and Print Results ---
# names = get_names_with_path(json_data)
# for name in names:
#   print(name)

# import json

# def get_names_with_path(data):
#     """Extracts names from a hierarchical JSON structure, building paths for
#     items with children. Ignores the root element if its name is '.'.

#     Args:
#         data: The hierarchical JSON data.

#     Returns:
#         A list of names with paths.
#     """

#     names_with_path = []
#     stack = [(data, "")]  # Start with the root and an empty path

#     while stack:
#         item, path = stack.pop()

#         # Skip if it's the root element with name "."
#         if path == "" and item.get('name') == '.':
#             if item.get('children'):
#                 for child in item['children']:
#                     stack.append((child, path))
#             continue

#         current_name = f"{path}{item['name']}"

#         if item.get('children'):
#             # If the item has children, add its path
#             names_with_path.append(current_name)
#             # Add children to the stack for processing with the updated path
#             for child in item['children']:
#                 stack.append((child, current_name + "/"))
#         else:
#             # If no children, just add the name
#             names_with_path.append(current_name)

#     return names_with_path

# # --- Dynamic Input ---
# # 1. From a JSON file:
# file_path = input("Enter the path to your JSON file: ")
# with open(file_path, 'r') as f:
#     json_data = json.load(f)

# # 2. Or, directly from user input as a string:
# # json_string = input("Enter your JSON data: ")
# # json_data = json.loads(json_string)

# # --- Generate JSON Schema ---
# names_with_path = get_names_with_path(json_data)
# schemas = {
#     "type": "object",
#     "properties": {},
#     "required": names_with_path
# }

# for name in names_with_path:
#     schemas['properties'][name] = {"type": "string"} 

# # --- Output ---
# print(json.dumps(schemas, indent=4))

import json

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

# --- Dynamic Input ---
file_path = input("Enter the path to your JSON file: ")
with open(file_path, 'r') as f:
    json_data = json.load(f) # Make sure this line is executed

# --- Extract data and create schema ---
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
    if name == "Material":  # Example: Add 'enum' for specific values
        property_schema["enum"] = ["Steel", "18-8 Stainless", "Stainless Steel", "Brass", "Nylon"]

    # Add more conditions and properties as needed based on your requirements

    # Assign the property schema
    schema_properties[name] = property_schema

# Create the JSON schema
schema = {
    "type": "object",
    "properties": schema_properties
}

# --- Output ---
print(json.dumps(schema, indent=4)) 