import requests
import json
import os
import pandas as pd
import numpy as np

def parse_json_response(response_text):
    """Parses a text response to extract and load a JSON object."""
    try:
        start_json = response_text.find("{")
        end_json = response_text.rfind("}")

        if start_json != -1 and end_json != -1:
            response_text = response_text[start_json:end_json + 1].strip() #Remove leading and trailing whitespaces.
            return json.loads(response_text)
        else:
            print("Warning: JSON object not found in response.")
            return None  # Or raise a custom exception
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Original response: {response_text}") #Print the original text for debugging.
        return None
    except Exception as e:
        print(f"Unexpected error parsing response: {e}")
        return None

# API 密钥（从环境变量中获取）
api_key = 'sk-7aecbf7b649344f6adb765f1b6cbc7a0'

# API 端点
url = "https://api.deepseek.com/v1/chat/completions"

def generate_dataset_columns(description):
    """
    使用 API 生成数据集列及其关联关系。

    Args:
        description (str): 数据集的描述。

    Returns:
        dict: 包含列及其关联关系的字典。
    """

    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a dataset column generator that respects constraints."
            },
            {
                "role": "user",
                "content": f"""
                Based on the following dataset description, generate possible columns (seed cols) and related columns for each seed col. 
                However, please follow these constraints:

                1. The total number of seed cols and related cols combined should be 20.
                2. Each seed col should have a maximum of 3 related cols.
                3. Include numerical columns where appropriate, such as 'salary', 'bonus', 'age', etc.
                4. If a seed column is numerical, make sure related columns are also numerical if applicable.
                5. Include categorical columns like 'country' and 'city' where appropriate.
                6. Ensure logical relationships between categorical columns like 'country' and 'city' (e.g., if country is 'USA', city should be 'New York' or 'Los Angeles').

                Dataset Description: {description}

                Please return the result in JSON format, as follows:
                {{
                    "salary": ["bonus", "total_salary"],
                    "age": ["years_of_experience"],
                    "product_price":["discount","final_price"],
                    "country": ["city"]
                }}
                """
            }
        ]
    })

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # 检查 HTTP 错误

        data = response.json()
        content = data['choices'][0]['message']['content'].strip()
        print(f"Original content: {content}")
        data = parse_json_response(content)


        # Enforce constraints and add numerical type hints
        # Enforce constraints after generation
        enforced_data = {}
        total_cols = 0
        for seed_col, related_cols in data.items():
            if total_cols >= 20:
                break  # Stop if total cols exceeds 10
            enforced_data[seed_col] = related_cols[:3]  # Limit to 3 related cols
            total_cols += 1 + len(related_cols[:3])  # Count seed col and limited related cols
        return enforced_data


    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None



def main():
    description = input("Enter dataset description: ")
    columns = generate_dataset_columns(description)

    if columns:
        with open("dataset_columns2.json", "w", encoding="utf-8") as f:
            json.dump(columns, f, ensure_ascii=False, indent=4)
        print("Dataset columns saved to dataset_columns.json.")
    else:
        print("Failed to generate dataset columns.")



if __name__ == "__main__":
    main()