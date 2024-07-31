from cx_Freeze import setup, Executable

# Define the application and its dependencies
build_exe_options = {
    "packages": [],
    "include_files": ["jsonSchemaGenerator.ico"],  # Include additional files like icons
}

setup(
    name="Json Schema Generator",
    version="1.0",
    description="This Application is used to create JSON Schema ",
    options={"build_exe": build_exe_options},
    executables=[Executable("json_schema_generator.py", base="Win32GUI", icon="jsonSchemaGenerator.ico")]
)
