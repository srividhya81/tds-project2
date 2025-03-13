from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import pandas as pd
import numpy as np
import zipfile
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import requests
from datetime import datetime, timedelta
import json
import hashlib
from github import Github

import sqlite3

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def send_request(email: str):
    try:
        response = requests.get('https://httpbin.org/get', params={'email': email})
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def find_hidden_input(url: str = 'https://exam.sanand.workers.dev/tds-2025-01-ga1'):
    try:
        # Set up the Selenium WebDriver (make sure you have the appropriate driver installed)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        # Navigate to the URL
        driver.get(url)

        # Find the hidden input element
        hidden_input = driver.find_element(By.XPATH, '//input[@type="hidden"]')
        hidden_value = hidden_input.get_attribute('value')

        # Close the WebDriver
        driver.quit()

        return {"hidden_value": hidden_value}
    except Exception as e:
        return {"error": str(e)}

def run_vscode():
    try:
        # Run the 'code -s' command
        result = subprocess.run(['code', '-s'], capture_output=True, text=True)
        if result.returncode == 0:
            return {"output": result.stdout}
        else:
            return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def download_and_format_readme():
    try:
        # Download the README.md file
        url = 'https://example.com/README.md'
        subprocess.run(['curl', '-o', 'README.md', url], check=True)

        # Run the prettier command
        result = subprocess.run(['npx', '-y', 'prettier@3.4.2', 'README.md', '|', 'sha256sum'], capture_output=True, text=True, check=True)
        return {'output': result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {'error': str(e)}

def execute_excel_formula(formula: str = Form(...)):
    try:
        # Create a new Excel workbook and sheet
        wb = openpyxl.Workbook()
        ws = wb.active

        # Sample data to be used in the formula
        data = [14,4,2,1,11,2,10,2,12,13,14,8,10,4,11,0]
        for i, value in enumerate(data, start=1):
            ws.cell(row=1, column=i, value=value)

        # Write the formula to a cell
        ws['A2'] = formula

        # Save the workbook to a temporary file
        file_location = "/tmp/formula.xlsx"
        wb.save(file_location)

        # Open the workbook and evaluate the formula
        wb = openpyxl.load_workbook(file_location, data_only=True)
        ws = wb.active
        result = ws['A2'].value

        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def write_google_sheets_formula(formula: str):
    try:
        # Create a new Excel workbook and sheet
        wb = openpyxl.Workbook()
        ws = wb.active

        # Write the formula to a cell
        ws['A1'] = formula

        # Save the workbook to a temporary file
        file_location = "/tmp/google_sheets_formula.xlsx"
        wb.save(file_location)

        return {"message": "Formula written to Excel file", "file_location": file_location}
    except Exception as e:
        return {"error": str(e)}

def write_excel_formula(formula: str):
    try:
        # Create a new Excel workbook and sheet
        wb = openpyxl.Workbook()
        ws = wb.active

        # Sample data to be used in the formula
        data = [14,4,2,1,11,2,10,2,12,13,14,8,10,4,11,0]
        for i, value in enumerate(data, start=1):
            ws.cell(row=1, column=i, value=value)

        # Write the formula to a cell
        ws['A2'] = formula

        # Save the workbook to a temporary file
        file_location = "/tmp/formula.xlsx"
        wb.save(file_location)

        # Open the workbook and evaluate the formula
        wb = openpyxl.load_workbook(file_location, data_only=True)
        ws = wb.active
        result = ws['A2'].value

        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def count_weekdays_in_range(start_date: str, end_date: str, weekday: str) -> int:
    try:
        # Convert input strings to datetime objects
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        # Define the weekday mapping
        weekdays = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }

        # Get the weekday number
        weekday_num = weekdays[weekday.lower()]

        # Count the number of specified weekdays in the date range
        count = 0
        current_date = start
        while current_date <= end:
            if current_date.weekday() == weekday_num:
                count += 1
            current_date += timedelta(days=1)

        return count
    except Exception as e:
        return {'error': str(e)}

def get_answer_from_csv(zip_url: str):
    try:
        # Download the zip file
        zip_path = '/tmp/extract.zip'
        subprocess.run(['curl', '-o', zip_path, zip_url], check=True)

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('/tmp')

        # Read the CSV file
        csv_path = '/tmp/extract.csv'
        df = pd.read_csv(csv_path)

        # Get the value in the 'answer' column
        answer_value = df['answer'].iloc[0]

        return {'answer': answer_value}
    except Exception as e:
        return {'error': str(e)}

def sort_json_array(json_array):
    try:
        # Sort the JSON array by age and then by name
        sorted_array = sorted(json_array, key=lambda x: (x['age'], x['name']))
        return json.dumps(sorted_array, separators=(',', ':'))
    except Exception as e:
        return {'error': str(e)}

def convert_to_json_and_hash(file_path: str):
    try:
        # Read the contents of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Convert the lines into a JSON object
        json_object = {}
        for line in lines:
            key, value = line.strip().split('=')
            json_object[key] = value

        # Convert the JSON object to a string
        json_string = json.dumps(json_object, separators=(',', ':'))

        # Calculate the hash of the JSON string
        hash_object = hashlib.sha256(json_string.encode())
        hash_hex = hash_object.hexdigest()

        return {'hash': hash_hex}
    except Exception as e:
        return {'error': str(e)}

def sum_data_value_attributes(url: str = 'https://exam.sanand.workers.dev/tds-2025-01-ga1'):
    try:
        # Set up the Selenium WebDriver (make sure you have the appropriate driver installed)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        # Navigate to the URL
        driver.get(url)

        # Find all <div> elements with the class 'foo'
        div_elements = driver.find_elements(By.CSS_SELECTOR, 'div.foo')

        # Sum the data-value attributes
        total_sum = sum(int(div.get_attribute('data-value')) for div in div_elements)

        # Close the WebDriver
        driver.quit()

        return {'sum': total_sum}
    except Exception as e:
        return {'error': str(e)}

def sum_values_from_files(zip_url: str):
    try:
        # Download the zip file
        zip_path = '/tmp/data_files.zip'
        subprocess.run(['curl', '-o', zip_path, zip_url], check=True)

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('/tmp')

        # Define the file paths
        data1_path = '/tmp/data1.csv'
        data2_path = '/tmp/data2.csv'
        data3_path = '/tmp/data3.txt'

        # Read the files with the correct encoding
        data1 = pd.read_csv(data1_path, encoding='cp1252')
        data2 = pd.read_csv(data2_path, encoding='utf-8')
        data3 = pd.read_csv(data3_path, encoding='utf-16', sep='\t')

        # Concatenate the dataframes
        data = pd.concat([data1, data2, data3])

        # Filter the rows where the symbol matches ” OR ž OR …
        filtered_data = data[data['symbol'].isin(['”', 'ž', '…'])]

        # Sum the values
        total_sum = filtered_data['value'].sum()

        return {'sum': total_sum}
    except Exception as e:
        return {'error': str(e)}

def create_github_repo_and_commit(email: str, github_token: str, repo_name: str):
    try:
        # Authenticate to GitHub
        g = Github(github_token)
        user = g.get_user()

        # Create a new repository
        repo = user.create_repo(repo_name, public=True)

        # Create the email.json file
        email_data = {"email": email}
        with open("/tmp/email.json", "w") as f:
            json.dump(email_data, f)

        # Commit and push the file to the repository
        repo.create_file("email.json", "Initial commit", json.dumps(email_data))

        # Get the raw URL of the email.json file
        raw_url = f"https://raw.githubusercontent.com/{user.login}/{repo_name}/main/email.json"

        return {"raw_url": raw_url}
    except Exception as e:
        return {"error": str(e)}

def replace_iitm_with_iit_madras(zip_url: str):
    try:
        # Download the zip file
        zip_path = '/tmp/replace_iitm.zip'
        subprocess.run(['curl', '-o', zip_path, zip_url], check=True)

        # Unzip the file into a new folder
        extract_path = '/tmp/replace_iitm_folder'
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Replace all occurrences of IITM with IIT Madras in all files
        for root, _, files in os.walk(extract_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                content = re.sub(r'IITM', 'IIT Madras', content, flags=re.IGNORECASE)
                with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)

        # Run the cat * | sha256sum command in the folder
        result = subprocess.run(['bash', '-c', f'cd {extract_path} && cat * | sha256sum'], capture_output=True, text=True)
        return {'sha256sum': result.stdout.strip()}
    except Exception as e:
        return {'error': str(e)}

def calculate_total_sales(db_path: str, ticket_type: str):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the SQL query to calculate total sales for the specified ticket type
        query = f"""
        SELECT SUM(units * price) AS total_sales
        FROM tickets
        WHERE LOWER(type) = '{ticket_type.lower()}'
        """
        cursor.execute(query)
        result = cursor.fetchone()

        # Close the database connection
        conn.close()

        return {'total_sales': result[0]}
    except Exception as e:
        return {'error': str(e)}

def compare_files(zip_url: str, comparison_type: str):
    try:
        # Download the zip file
        zip_path = '/tmp/compare_files.zip'
        subprocess.run(['curl', '-o', zip_path, zip_url], check=True)

        # Unzip the file into a new folder
        extract_path = '/tmp/compare_files_folder'
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Read the contents of a.txt and b.txt
        with open(os.path.join(extract_path, 'a.txt'), 'r') as file_a:
            lines_a = file_a.readlines()
        with open(os.path.join(extract_path, 'b.txt'), 'r') as file_b:
            lines_b = file_b.readlines()

        # Compare the lines based on the comparison type
        if comparison_type == 'different':
            different_lines = sum(1 for a, b in zip(lines_a, lines_b) if a != b)
            return {'different_lines': different_lines}
        elif comparison_type == 'similar':
            similar_lines = sum(1 for a, b in zip(lines_a, lines_b) if a == b)
            return {'similar_lines': similar_lines}
        else:
            return {'error': 'Invalid comparison type'}
    except Exception as e:
        return {'error': str(e)}

import re

def process_and_rename_files(zip_url: str):
    try:
        # Download the zip file
        zip_path = '/tmp/process_files.zip'
        subprocess.run(['curl', '-o', zip_path, zip_url], check=True)

        # Unzip the file into a new folder
        extract_path = '/tmp/process_files_folder'
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Create an empty folder to move all files into
        target_path = '/tmp/processed_files_folder'
        os.makedirs(target_path, exist_ok=True)

        # Move all files under folders into the empty folder
        for root, _, files in os.walk(extract_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    subprocess.run(['mv', file_path, target_path], check=True)

        # Rename all files replacing each digit with the next
        for file in os.listdir(target_path):
            new_name = re.sub(r'\d', lambda x: str((int(x.group()) + 1) % 10), file)
            os.rename(os.path.join(target_path, file), os.path.join(target_path, new_name))

        # Run the grep . * | LC_ALL=C sort | sha256sum command in the folder
        result = subprocess.run(['bash', '-c', f'cd {target_path} && grep . * | LC_ALL=C sort | sha256sum'], capture_output=True, text=True)
        return {'sha256sum': result.stdout.strip()}
    except Exception as e:
        return {'error': str(e)}

def generate_markdown_documentation() -> str:
    markdown_content = '''
# Analysis of Daily Steps

## Introduction

This document presents an **imaginary** analysis of the number of steps walked each day for a week, comparing over time and with friends.

## Methodology

*Note:* The data was collected using a fitness tracker and compared with friends using a social fitness app.

## Data Collection

The data was collected over a period of one week. The following steps were taken:

1. Data was recorded daily using a fitness tracker.
2. Data was synced with the social fitness app.
3. Data was compared with friends' data.

## Results

The table below shows the number of steps walked each day:

| Day       | Steps  |
|-----------|--------|
| Monday    | 10,000 |
| Tuesday   | 12,000 |
| Wednesday | 8,000  |
| Thursday  | 11,000 |
| Friday    | 9,500  |
| Saturday  | 13,000 |
| Sunday    | 7,500  |

## Comparison with Friends

The following code snippet shows how the data was processed:

```
import pandas as pd

# Sample data
data = {
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'Steps': [10000, 12000, 8000, 11000, 9500, 13000, 7500]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate average steps
average_steps = df['Steps'].mean()
print(f'Average steps: {average_steps}')
```

## Insights

- The highest number of steps was recorded on *Saturday*.
- The lowest number of steps was recorded on *Sunday*.
- The average number of steps per day was calculated using the inline code `df['Steps'].mean()`.

## Conclusion

> This analysis provides insights into daily step counts and comparisons with friends. For more information, visit the [social fitness app](https://example.com).

![Fitness Tracker](https://example.com/image.jpg)
'''
    return markdown_content

def compress_image(image_path: str, output_path: str):
    from PIL import Image
    import os
    
    # Open the image file
    with Image.open(image_path) as img:
        # Save the image with the highest compression level
        img.save(output_path, format='PNG', optimize=True)
        
    # Check the file size
    if os.path.getsize(output_path) > 1500:
        raise ValueError('Compressed image size exceeds 1,500 bytes')

def publish_github_pages(email: str, github_token: str, repo_name: str):
    try:
        # Authenticate to GitHub
        g = Github(github_token)
        user = g.get_user()

        # Create a new repository
        repo = user.create_repo(repo_name, public=True)

        # Create the index.html file with the email obfuscated
        html_content = f"""
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <title>My Work</title>
        </head>
        <body>
            <h1>Showcase of My Work</h1>
            <p>Email: <!--email_off-->{email}<!--/email_off--></p>
        </body>
        </html>
        """
        with open('/tmp/index.html', 'w') as f:
            f.write(html_content)

        # Commit and push the file to the repository
        repo.create_file('index.html', 'Initial commit', html_content)

        # Enable GitHub Pages
        repo.edit(has_wiki=False, has_projects=False, has_downloads=False, default_branch='main')
        repo.create_pages_site(source='main')

        # Get the GitHub Pages URL
        pages_url = f"https://{user.login}.github.io/{repo_name}/"
        return {"pages_url": pages_url}
    except Exception as e:
        return {"error": str(e)}

def run_colab_code():
    import hashlib
    import requests
    # from google.colab import auth
    from oauth2client.client import GoogleCredentials

    auth.authenticate_user()
    creds = GoogleCredentials.get_application_default()
    token = creds.get_access_token().access_token
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"alt": "json"},
        headers={"Authorization": f"Bearer {token}"}
    )
    email = response.json()["email"]
    result = hashlib.sha256(f"{email} {creds.token_expiry.year}".encode()).hexdigest()[-5:]
    return result

def count_light_pixels(image_path: str, threshold: float = 0.05) -> int:
    import numpy as np
    from PIL import Image
    import colorsys

    # Open the image file
    image = Image.open(image_path)

    # Convert the image to RGB and normalize
    rgb = np.array(image) / 255.0

    # Calculate lightness for each pixel
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)

    # Count the number of pixels with lightness greater than the threshold
    light_pixels = np.sum(lightness > threshold)

    return light_pixels

import json

@app.get("/api")
def get_marks(name: str):
    with open('marks.json', 'r') as f:
        data = json.load(f)
    marks = [data.get(n, 0) for n in name.split(',')]
    return {"marks": marks}

functions_dict = {
    "send_request": send_request,
    "find_hidden_input": find_hidden_input,
    "run_vscode": run_vscode,
    "execute_excel_formula": execute_excel_formula,
    "download_and_format_readme": download_and_format_readme,
    "write_google_sheets_formula": write_google_sheets_formula,
    "write_excel_formula": write_excel_formula,
    "count_weekdays_in_range": count_weekdays_in_range,
    "get_answer_from_csv": get_answer_from_csv,
    "sort_json_array": sort_json_array,
    "convert_to_json_and_hash": convert_to_json_and_hash,
    "sum_data_value_attributes": sum_data_value_attributes,
    "sum_values_from_files": sum_values_from_files,
    "create_github_repo_and_commit": create_github_repo_and_commit,
    "replace_iitm_with_iit_madras": replace_iitm_with_iit_madras,
    "calculate_total_sales": calculate_total_sales,
    "compare_files": compare_files,
    "process_and_rename_files": process_and_rename_files,
    "generate_markdown_documentation": generate_markdown_documentation,
    "compress_image": compress_image,
    "publish_github_pages": publish_github_pages,
    "run_colab_code": run_colab_code,
    "count_light_pixels": count_light_pixels,
    "get_marks": get_marks
}

function_descriptions = [
    "Run VSCode",
    "Send a request",
    "Execute an Excel formula",
    "Download and format README",
    "Write Google Sheets formula",
    "Write Excel formula",
    "Count weekdays in range",
    "Get answer from CSV",
    "Sort JSON array",
    "Convert to JSON and hash",
    "Sum data-value attributes",
    "Sum values from files",
    "Create GitHub repo and commit",
    "Replace IITM with IIT Madras and calculate sha256sum",
    "Calculate total sales for specified ticket type",
    "Compare lines between files",
    "Process and rename files and calculate sha256sum",
    "Generate Markdown documentation",
    "Compress an image losslessly to less than 1,500 bytes",
    "Publish a page using GitHub Pages that showcases your work",
    "Run a program on Google Colab to get a 5-character string",
    "Count the number of pixels with a certain minimum brightness in an image",
    "Get marks of students"
]

@app.post("/api/")
def handle_api_request(question: str = Form(...), file: UploadFile = File(None)):
    try:
        # Calculate similarity between the question and function descriptions using embeddings
        question_embedding = model.encode(question)
        function_embeddings = model.encode(function_descriptions)
        cosine_similarities = cosine_similarity([question_embedding], function_embeddings).flatten()
        most_similar_function_index = cosine_similarities.argmax()
        most_similar_function = list(functions_dict.values())[most_similar_function_index]

        # Call the most similar function
        if most_similar_function == execute_excel_formula and file and file.filename.endswith('.xlsx'):
            formula = question.split("formula: ")[1]
            return execute_excel_formula(formula)
        elif most_similar_function == find_hidden_input and "url: " in question:
            url = question.split("url: ")[1]
            return find_hidden_input(url)
        elif most_similar_function == send_request:
            email = question.split("email: ")[1]
            return send_request(email)
        elif most_similar_function == run_vscode:
            return run_vscode()
        elif most_similar_function == download_and_format_readme:
            return download_and_format_readme()
        elif most_similar_function == write_google_sheets_formula:
            formula = question.split("formula: ")[1]
            return write_google_sheets_formula(formula)
        elif most_similar_function == write_excel_formula:
            formula = question.split("formula: ")[1]
            return write_excel_formula(formula)
        elif most_similar_function == count_weekdays_in_range:
            start_date, end_date, weekday = question.split(" ")[1:4]
            return count_weekdays_in_range(start_date, end_date, weekday)
        elif most_similar_function == get_answer_from_csv and "url: " in question:
            zip_url = question.split("url: ")[1]
            return get_answer_from_csv(zip_url)
        elif most_similar_function == sort_json_array:
            json_array = json.loads(question.split("json: ")[1])
            return sort_json_array(json_array)
        elif most_similar_function == convert_to_json_and_hash and file and file.filename.endswith('.txt'):
            file_path = f'/tmp/{file.filename}'
            with open(file_path, 'wb') as f:
                f.write(file.file.read())
            return convert_to_json_and_hash(file_path)
        elif most_similar_function == sum_data_value_attributes:
            return sum_data_value_attributes()
        elif most_similar_function == sum_values_from_files and "url: " in question:
            zip_url = question.split("url: ")[1]
            return sum_values_from_files(zip_url)
        elif most_similar_function == create_github_repo_and_commit:
            email = question.split("email: ")[1]
            github_token = question.split("token: ")[1]
            repo_name = question.split("repo: ")[1]
            return create_github_repo_and_commit(email, github_token, repo_name)
        elif most_similar_function == replace_iitm_with_iit_madras and "url: " in question:
            zip_url = question.split("url: ")[1]
            return replace_iitm_with_iit_madras(zip_url)
        elif most_similar_function == calculate_total_sales and "db_path: " in question:
            db_path, ticket_type = question.split("db_path: ")[1].split(" ticket_type: ")
            return calculate_total_sales(db_path, ticket_type)
        elif most_similar_function == compare_files and "url: " in question:
            zip_url, comparison_type = question.split("url: ")[1].split(" comparison_type: ")
            return compare_files(zip_url, comparison_type)
        elif most_similar_function == process_and_rename_files and "url: " in question:
            zip_url = question.split("url: ")[1]
            return process_and_rename_files(zip_url)
        elif most_similar_function == generate_markdown_documentation:
            return generate_markdown_documentation()
        elif most_similar_function == compress_image and file and file.filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = f'/tmp/{file.filename}'
            output_path = f'/tmp/compressed_{file.filename}'
            with open(image_path, 'wb') as f:
                f.write(file.file.read())
            compress_image(image_path, output_path)
            return {"message": "Image compressed successfully", "output_path": output_path}
        elif most_similar_function == publish_github_pages:
            email = question.split("email: ")[1]
            github_token = question.split("token: ")[1]
            repo_name = question.split("repo: ")[1]
            return publish_github_pages(email, github_token, repo_name)
        elif most_similar_function == run_colab_code:
            return {"result": run_colab_code()}
        elif most_similar_function == count_light_pixels and file and file.filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = f'/tmp/{file.filename}'
            with open(image_path, 'wb') as f:
                f.write(file.file.read())
            threshold = float(question.split("threshold: ")[1]) if "threshold: " in question else 0.05
            light_pixels = count_light_pixels(image_path, threshold)
            return {"light_pixels": light_pixels}
        elif most_similar_function == get_marks:
            name = question.split("name: ")[1]
            return get_marks(name)
        else:
            return {"error": "Unsupported question format or file type"}
    except Exception as e:
        return {"error": str(e)}


