# Controllable Table Data Synthesis with Natural Language and Knowledge Base

This project provides a pipeline for generating structured table datasets using natural language descriptions and an optional knowledge base for controlled constraints. The workflow consists of three sequential steps:

1. **`generate_json.py`** - Accepts a natural language description of the desired table dataset and generates a JSON file representing column relationships.
2. **`generate_python.py`** - Takes the JSON file as input, optionally incorporating a knowledge base to enforce controlled constraints on the synthesized data.
3. **`generate_dataset.py`** - Uses the processed JSON and constraints to generate the final dataset.

## Workflow

1. **Define the dataset**: Run `generate_json.py` with a textual description of the table data you want to synthesize.
2. **Process constraints**: Use `generate_python.py` to process the JSON output, optionally integrating domain-specific knowledge for enhanced control.
3. **Generate the dataset**: Execute `generate_dataset.py` to synthesize the structured data.

## File Descriptions

### `generate_json.py`
**Functionality:**
- Accepts a text description of the target dataset.
- Produces a JSON file defining column relationships.

**Usage:**
```bash
python generate_json.py --description "Your dataset description here"
```

### `generate_python.py`
**Functionality:**
- Processes the JSON file generated in the first step.
- Optionally integrates a knowledge base to impose constraints on the synthesized data.

**Usage:**
```bash
python generate_python.py --json_file generated_structure.json [--knowledge_base knowledge_base.json]
```

### `generate_dataset.py`
**Functionality:**
- Generates the final table dataset based on the structured JSON and optional constraints.

**Usage:**
```bash
python generate_dataset.py --json_file processed_structure.json
```

## Dependencies

The project requires the following Python libraries. It is recommended to use Python 3.8 or later.

```bash
pip install -r requirements.txt
```

Ensure all dependencies are installed before running the scripts.

## File Structure
```
Project Root
│   README.md
│   requirements.txt
│
└───scripts
    │   generate_json.py
    │   generate_python.py
    │   generate_dataset.py
```

## Notes

- Ensure that all scripts are executed in the correct sequence for proper dataset synthesis.
- The knowledge base is optional but improves data generation control.
- Refer to inline comments within each script for additional details on parameters and configurations.

## Contributors

For any issues or suggestions, feel free to reach out to the project maintainers.

---

Thank you for using this project! We hope it helps with your work.

