import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import Qt
import json
from genson import SchemaBuilder

class JsonSchemaGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout setup
        layout = QVBoxLayout()

        # Input label and text area
        self.input_label = QLabel("Input JSON:")
        layout.addWidget(self.input_label)

        self.json_input = QTextEdit(self)
        self.json_input.setPlaceholderText("Enter your JSON data here...")
        layout.addWidget(self.json_input)

        # Button to generate schema
        self.generate_btn = QPushButton('Generate Schema', self)
        self.generate_btn.clicked.connect(self.generate_schema)
        layout.addWidget(self.generate_btn)

        # Output label and text area
        self.output_label = QLabel("Generated Schema:")
        layout.addWidget(self.output_label)

        self.schema_output = QTextEdit(self)
        self.schema_output.setPlaceholderText("The generated JSON schema will appear here...")
        self.schema_output.setReadOnly(True)
        layout.addWidget(self.schema_output)

        # Set main layout
        self.setLayout(layout)
        self.setWindowTitle('JSON Schema Generator')
        self.setGeometry(300, 300, 600, 400)

    def generate_schema(self):
        json_data = self.json_input.toPlainText()
        try:
            data = json.loads(json_data)
            builder = SchemaBuilder()
            builder.add_object(data)
            schema = builder.to_schema()
            self.schema_output.setText(json.dumps(schema, indent=4))
        except json.JSONDecodeError:
            self.schema_output.setText("Invalid JSON data. Please check your input.")
        except Exception as e:
            self.schema_output.setText(f"Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JsonSchemaGenerator()
    ex.show()
    sys.exit(app.exec_())
