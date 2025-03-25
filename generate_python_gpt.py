import json
import os
import subprocess
import re
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="",
    base_url=""
)


def extract_python_code(response_text):
    """
    从响应文本中提取 Python 代码块。

    Args:
        response_text (str): 响应文本。

    Returns:
        str: 提取的 Python 代码，如果未找到则返回 None。
    """
    print("response_text:",response_text)
    pattern = r"`python\s*(.*?)\s*`"
    match = re.search(pattern, response_text, re.DOTALL)
    print("match:",match)
    if match:
        return match.group(1).strip()
    else:
        return None


def generate_python_script(json_data, description, num_rows=10000):
    """
    根据给定的 JSON 结构生成 Python 脚本。

    Args:
        json_data (dict): 包含列及其关联关系的 JSON 数据。
        num_rows (int): 生成的行数。

    Returns:
        str: 生成的 Python 脚本。
    """

    prompt = f"""
The following JSON structure depicts the columns of a dataset and the relationships between them:

{json.dumps(json_data)}

Generate a Python script to build a Pandas DataFrame with {num_rows} rows based on this structure. You must strictly follow the guidelines below, with the 'Other constraints' being of utmost importance and requiring meticulous attention.

### 1. Data Types
- When a column name appears as a key in the JSON, figure out its data - type according to the context and relationships specified.
- For column names in the JSON values, determine their data - types based on the given context and relationships.
- If a column is neither a key nor a value in the JSON and has no connection to a numerical key, consider it a categorical (string) column.
- A column in the JSON keys that is related to numerical values should be regarded as a numerical column.
- If a column in the JSON keys is related to categorical values, classify it as a categorical column.

### 2. Relationships
- Deduce the numerical relationships between columns from the provided JSON structure.
- Here are some examples for better understanding:
  - If "total_salary" is related to "base", "bonus", and "commission", set "total_salary" equal to the sum of "base", "bonus", and "commission" (i.e., "total_salary" = "base" + "bonus" + "commission").
  - If "final_price" is related to "product_price" and "discount", calculate "final_price" as "product_price" minus "discount" (i.e., "final_price" = "product_price" - "discount").
  - When "years_of_experience" is related to "age", derive "years_of_experience" from "age" (e.g., "years_of_experience" = "age" - a random number).
  - If "retirement_age" is related to "age", compute "retirement_age" based on "age" (e.g., "retirement_age" = 65 - "age").

### 3. Conditional Logic
- If "country" is "China", "city" should be a Chinese city (e.g., "Beijing", "Shanghai").
- If "country" is "USA", "city" should be an American city (e.g., "New York", "Los Angeles").
- If "country" is "France", "city" should be a French city (e.g., "Paris", "Marseille").

### 4. Data Ranges
- Generate data within reasonable ranges for numerical columns.
- Here are some example ranges:
  - "salary": 30,000 to 150,000
  - "base": 20,000 to 100,000
  - "bonus": 0 to 50,000
  - "commission": 0 to 20,000
  - "years_of_experience": 0 to 40
  - "discount": 0 to 500

### 5. Output
- Save the generated DataFrame to a CSV file named "generated_dataset.csv".
- Provide only the Python code without any explanations or additional text.

### 6. Other constraints
This is the most crucial part of the task. Carefully analyze the {description} to extract all constraints relevant to columns that exist in the {json_data}. In cases where there are multiple constraints for the same numerical column, such as different ranges for the "age" column, you must calculate the intersection of these constraints and generate data that falls within this intersection. For example, if the `description` provides an age range of 50 to 60 and another range of 55 to 65 for the "age" column, the generated "age" data should be in the range of 55 to 60， you should calculate the intersection precisely. Any oversight or incorrect implementation of these constraints will lead to an invalid solution.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a Python script generator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        # model="o1"
        # model="o3-mini"
        model="gpt-4o"
    )
    content = chat_completion.choices[0].message.content.strip()
    python_code = extract_python_code(content)
    return python_code


with open("dataset_columns2.json", "r") as f:
    json_data = json.load(f)

# 生成 Python 脚本
description_file = "description.txt"
content = None
if os.path.exists(description_file):
    with open(description_file, 'r') as file:
        content = file.read()

python_script = generate_python_script(json_data, content)

if python_script:
    # 保存 Python 脚本到文件
    with open("generate_dataset.py", "w") as f:
        f.write(python_script)

    # 运行 Python 脚本
    try:
        subprocess.run(["python", "generate_dataset.py"], check=True)
        print("Dataset generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
else:
    print("Failed to generate Python script.")
    
