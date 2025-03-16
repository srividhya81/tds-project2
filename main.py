from fastapi import FastAPI, UploadFile, File, Form, Request, Query
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
from bs4 import BeautifulSoup

import sqlite3

import tiktoken

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST", "GET"],  # Allow OPTIONS, POST, and GET methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, students of TDS-2025-01!, Post your queries here."}

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

def execute_excel_formula(formula: str = Form(...), data: str = Form(...)):
    try:
        # Convert the data string to a list of integers
        data = list(map(int, data.split(',')))

        # Evaluate the formula using Python
        result = eval(formula)

        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def write_google_sheets_formula(formula: str, data: str):
    try:
        # Convert the data string to a list of integers
        data = list(map(int, data.split(',')))

        # Evaluate the formula using Python
        result = eval(formula)

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

import base64

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

    # Convert the compressed image to base64 encoding
    with open(output_path, 'rb') as img_file:
        base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')

    return base64_encoded

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
        return {'error': str(e)}

def run_colab_code():
    import hashlib
    import requests
    import google.auth
    from oauth2client.client import GoogleCredentials

    from google.colab import auth
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

import docker

def create_and_push_docker_image(dockerhub_username: str, dockerhub_password: str, repo_name: str, tag: str = '23ds1000022') -> str:
    try:
        client = docker.from_env()

        # Build the Docker image
        image, build_logs = client.images.build(path='.', tag=f'{dockerhub_username}/{repo_name}:{tag}')

        # Log in to Docker Hub
        client.login(username=dockerhub_username, password=dockerhub_password)

        # Push the Docker image
        push_logs = client.images.push(dockerhub_username, repo_name, tag=tag)

        # Return the Docker image URL
        docker_image_url = f'https://hub.docker.com/repository/docker/{dockerhub_username}/{repo_name}/general'
        return docker_image_url
    except Exception as e:
        return {'error': str(e)}

import subprocess

def download_and_run_llamafile_model():
    try:
        # Download Llamafile
        subprocess.run(['curl', '-o', 'Llamafile', 'https://example.com/Llamafile'], check=True)
        subprocess.run(['chmod', '+x', 'Llamafile'], check=True)

        # Run the Llama-3.2-1B-Instruct.Q6_K.llamafile model
        subprocess.run(['./Llamafile', 'run', 'Llama-3.2-1B-Instruct.Q6_K.llamafile'], check=True)

        # Create a tunnel to the Llamafile server using ngrok
        ngrok_process = subprocess.Popen(['ngrok', 'http', '8000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ngrok_url = None
        while True:
            output = ngrok_process.stdout.readline().decode('utf-8')
            if 'url=' in output:
                ngrok_url = output.split('url=')[1].strip()
                break

        return {'ngrok_url': ngrok_url}
    except Exception as e:
        return {'error': str(e)}

import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/engines/gpt-4o-mini/completions"
    headers = {
        "Authorization": "Bearer dummy_api_key",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Analyze the sentiment of the text into GOOD, BAD, or NEUTRAL."},
            {"role": "user", "content": "j\nuCucnWF2maKq9ocMq2Ic WjXaN5 1XXI ubwVfqle  EWW"}
        ]
    }
    response = httpx.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

@app.post("/api/analyze_sentiment_code")
def get_analyze_sentiment_code():
    code = '''
import httpx

def analyze_sentiment():
    url = "https://api.openai.com/v1/engines/gpt-4o-mini/completions"
    headers = {
        "Authorization": "Bearer dummy_api_key",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Analyze the sentiment of the text into GOOD, BAD, or NEUTRAL."},
            {"role": "user", "content": "j\nuCucnWF2maKq9ocMq2Ic WjXaN5 1XXI ubwVfqle  EWW"}
        ]
    }
    response = httpx.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()
    '''
    return {"code": code}

import tiktoken

def count_tokens_and_valid_words(text: str):
    try:
        # Initialize the tokenizer
        enc = tiktoken.get_encoding("gpt-4o-mini")

        # Tokenize the text
        tokens = enc.encode(text)
        num_tokens = len(tokens)

        # Extract valid English words
        words = text.split(', ')
        valid_words = [word for word in words if word.isalpha()]

        return {"num_tokens": num_tokens, "valid_words": valid_words}
    except Exception as e:
        return {"error": str(e)}

def llm_text_extraction():
    json_body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Respond in JSON"
            },
            {
                "role": "user",
                "content": "Generate 10 random addresses in the US"
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "generate_us_addresses",
                    "description": "Generates 10 random addresses in the United States.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "addresses": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "zip": {
                                            "type": "number",
                                            "description": "The ZIP code of the address."
                                        },
                                        "city": {
                                            "type": "string",
                                            "description": "The city of the address."
                                        },
                                        "apartment": {
                                            "type": "string",
                                            "description": "The apartment or street address."
                                        }
                                    },
                                    "required": ["zip", "city", "apartment"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["addresses"],
                        "additionalProperties": False
                    }
                }
            }
        ]
    }
    return json_body

import base64
from fastapi import UploadFile

def llm_text_extraction_with_image(file: UploadFile):
    try:
        # Read the image file and encode it to base64
        image_data = file.file.read()
        base64_encoded_image = base64.b64encode(image_data).decode('utf-8')

        json_body = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract text from this image"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_encoded_image}"}
                        }
                    ]
                }
            ]
        }
        return json_body
    except Exception as e:
        return {"error": str(e)}

def generate_embedding_request(messages: list):
    try:
        json_body = {
            "model": "text-embedding-3-small",
            "input": messages
        }
        return json_body
    except Exception as e:
        return {"error": str(e)}

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def most_similar(embeddings: dict):
    try:
        phrases = list(embeddings.keys())
        vectors = np.array(list(embeddings.values()))

        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(vectors)

        # Find the indices of the maximum similarity (excluding diagonal)
        np.fill_diagonal(similarity_matrix, -np.inf)  # Exclude self-similarity
        max_indices = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)

        # Return the pair of phrases with the highest similarity
        return (phrases[max_indices[0]], phrases[max_indices[1]])
    except Exception as e:
        return {"error": str(e)}

@app.post("/similarity")
def compute_similarity(payload: dict):
    try:
        docs = payload.get("docs", [])
        query = payload.get("query", "")

        if not docs or not query:
            return {"error": "Both 'docs' and 'query' must be provided."}

        # Initialize the tokenizer
        enc = tiktoken.get_encoding("text-embedding-3-small")

        # Generate embeddings for documents and query
        doc_embeddings = [enc.encode(doc) for doc in docs]
        query_embedding = enc.encode(query)

        # Convert embeddings to numpy arrays
        doc_embeddings = np.array(doc_embeddings)
        query_embedding = np.array(query_embedding).reshape(1, -1)

        # Compute cosine similarity
        similarity_scores = cosine_similarity(query_embedding, doc_embeddings).flatten()

        # Get indices of the top 3 most similar documents
        top_indices = similarity_scores.argsort()[-3:][::-1]

        # Return the top 3 matches
        matches = [docs[i] for i in top_indices]
        return {"matches": matches}
    except Exception as e:
        return {"error": str(e)}

@app.get("/execute")
def execute_query(q: str):
    try:
        # Match the query to the appropriate function
        if match := re.match(r"What is the status of ticket (\d+)\?", q):
            ticket_id = int(match.group(1))
            return {"name": "get_ticket_status", "arguments": json.dumps({"ticket_id": ticket_id})}
        elif match := re.match(r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in Room ([A-Z])\.", q):
            date, time, meeting_room = match.groups()
            return {"name": "schedule_meeting", "arguments": json.dumps({"date": date, "time": time, "meeting_room": meeting_room})}
        elif match := re.match(r"Show my expense balance for employee (\d+)\.", q):
            employee_id = int(match.group(1))
            return {"name": "get_expense_balance", "arguments": json.dumps({"employee_id": employee_id})}
        elif match := re.match(r"Calculate performance bonus for employee (\d+) for (\d{4})\.", q):
            employee_id, current_year = map(int, match.groups())
            return {"name": "calculate_performance_bonus", "arguments": json.dumps({"employee_id": employee_id, "current_year": current_year})}
        elif match := re.match(r"Report office issue (\d+) for the (\w+) department\.", q):
            issue_code = int(match.group(1))
            department = match.group(2)
            return {"name": "report_office_issue", "arguments": json.dumps({"issue_code": issue_code, "department": department})}
        else:
            return {"error": "Query not recognized"}
    except Exception as e:
        return {"error": str(e)}

import requests
from bs4 import BeautifulSoup
import pandas as pd

def count_stat_from_cricinfo(page_number: int, stat_column: str):
    try:
        # Construct the URL for the given page number
        url = f"https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;page={page_number};template=results;type=batting"

        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the table containing the stats
        table = soup.find('table', class_='engineTable')
        if not table:
            return {"error": "Stats table not found on the page."}

        # Convert the table to a DataFrame
        df = pd.read_html(str(table))[0]

        # Check if the stat column exists
        if stat_column not in df.columns:
            return {"error": f"Column '{stat_column}' not found in the table."}

        # Sum the values in the specified column
        total_stat = df[stat_column].sum()

        return {"total": total_stat}
    except Exception as e:
        return {"error": str(e)}

def extract_movie_data(rating_filter: str, fields: list):
    try:
        # Construct the IMDb search URL based on the rating filter
        url = f"https://www.imdb.com/search/title/?user_rating={rating_filter}"

        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the movie containers
        movie_containers = soup.find_all('div', class_='lister-item mode-advanced')

        # Extract data for up to the first 25 movies
        movies = []
        for container in movie_containers[:25]:
            movie_data = {}

            # Extract the IMDb ID
            link = container.h3.a['href']
            movie_data['id'] = link.split('/title/tt')[1].split('/')[0]

            # Extract the title
            if 'title' in fields:
                movie_data['title'] = container.h3.a.text

            # Extract the year
            if 'year' in fields:
                year = container.h3.find('span', class_='lister-item-year').text
                movie_data['year'] = year.strip('()')

            # Extract the rating
            if 'rating' in fields:
                rating = container.find('div', class_='inline-block ratings-imdb-rating')
                movie_data['rating'] = rating['data-value'] if rating else None

            movies.append(movie_data)

        return movies
    except Exception as e:
        return {"error": str(e)}

import requests

def get_weather_forecast(city: str, api_key: str):
    try:
        # Step 1: Fetch the locationId for the city
        locator_url = "https://api.bbcweather.com/locator"
        locator_params = {
            "apiKey": api_key,
            "locale": "en",
            "filter": "city",
            "searchTerm": city
        }
        locator_response = requests.get(locator_url, params=locator_params)
        locator_response.raise_for_status()
        location_data = locator_response.json()

        # Extract locationId
        location_id = location_data["locationId"]

        # Step 2: Fetch the weather forecast using the locationId
        weather_url = f"https://api.bbcweather.com/weather/{location_id}"
        weather_params = {
            "apiKey": api_key
        }
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Step 3: Extract and transform the weather data
        forecasts = weather_data.get("forecasts", [])
        weather_forecast = {
            forecast["localDate"]: forecast["enhancedWeatherDescription"]
            for forecast in forecasts
        }

        return weather_forecast
    except Exception as e:
        return {"error": str(e)}

import requests

def get_min_latitude(city: str, country: str, parameter: str):
    try:
        # Construct the Nominatim API URL
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{city}, {country}",
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }

        # Fetch the geospatial data
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            return {"error": "No results found for the specified city and country."}

        # Extract the bounding box
        bounding_box = data[0].get("boundingbox", [])
        if not bounding_box:
            return {"error": "Bounding box not found in the response."}

        # Extract the required parameter (e.g., minimum latitude)
        if parameter == "min_latitude":
            return {"min_latitude": float(bounding_box[0])}
        elif parameter == "max_latitude":
            return {"max_latitude": float(bounding_box[1])}
        elif parameter == "min_longitude":
            return {"min_longitude": float(bounding_box[2])}
        elif parameter == "max_longitude":
            return {"max_longitude": float(bounding_box[3])}
        else:
            return {"error": "Invalid parameter specified."}
    except Exception as e:
        return {"error": str(e)}


import requests
import xml.etree.ElementTree as ET

def get_latest_hn_post(topic: str, min_points: int):
    try:
        # Fetch the latest Hacker News posts using the HNRSS API
        url = "https://hnrss.org/newest"
        response = requests.get(url)
        response.raise_for_status()

        # Parse the XML response
        root = ET.fromstring(response.content)

        # Iterate through the <item> elements
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            points = item.find("hn:points", namespaces={"hn": "https://hnrss.org/"}).text

            # Check if the title contains the topic and points meet the minimum threshold
            if topic.lower() in title.lower() and int(points) >= min_points:
                return link

        return {"error": "No matching post found."}
    except Exception as e:
        return {"error": str(e)}

import requests

def get_github_user_by_date(city: str, min_followers: int, github_token: str, date_type: str):
    try:
        # Construct the GitHub API URL
        url = "https://api.github.com/search/users"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json"
        }
        params = {
            "q": f"location:{city} followers:>{min_followers}",
            "sort": "joined",
            "order": "desc" if date_type == "newest" else "asc"
        }

        # Fetch the user data
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("items"):
            return {"error": "No users found matching the criteria."}

        # Get the user (first in the sorted list)
        user = data["items"][0]
        user_details_url = user["url"]

        # Fetch detailed user data
        user_response = requests.get(user_details_url, headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()

        # Extract the creation date
        created_at = user_data["created_at"]

        return {"user_created_at": created_at}
    except Exception as e:
        return {"error": str(e)}
    

import os
import subprocess

def create_github_action(email: str, github_repo_url: str):
    try:
        # Define the GitHub Actions workflow content
        workflow_content = f'''
name: Daily Commit

on:
  schedule:
    - cron: "0 0 * * *"  # Runs daily at midnight

jobs:
  daily-commit:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Git user
      run: |
        git config --global user.name "GitHub Action"
        git config --global user.email "{email}"

    - name: Make a commit
      run: |
        date > date.txt
        git add date.txt
        git commit -m "Daily commit"
        git push
'''

        # Create the .github/workflows directory if it doesn't exist
        workflows_dir = ".github/workflows"
        os.makedirs(workflows_dir, exist_ok=True)

        # Write the workflow file
        workflow_path = os.path.join(workflows_dir, "daily-commit.yml")
        with open(workflow_path, "w") as workflow_file:
            workflow_file.write(workflow_content)

        # Add, commit, and push the workflow file to the repository
        subprocess.run(["git", "add", workflow_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add daily commit GitHub Action"], check=True)
        subprocess.run(["git", "push"], check=True)

        return {"repository_url": github_repo_url}
    except Exception as e:
        return {"error": str(e)}


import tabula

def calculate_total_marks(file: UploadFile, subject: str, filter_subject: str, min_marks: int, group_range: tuple):
    try:
        # Save the uploaded PDF file temporarily
        pdf_path = f"/tmp/{file.filename}"
        with open(pdf_path, "wb") as f:
            f.write(file.file.read())

        # Extract tables from the PDF using Tabula
        tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True, pandas_options={"header": 0})

        # Combine all tables into a single DataFrame
        df = pd.concat(tables, ignore_index=True)

        # Ensure marks are numeric
        df[filter_subject] = pd.to_numeric(df[filter_subject], errors="coerce")
        df[subject] = pd.to_numeric(df[subject], errors="coerce")
        df["Group"] = pd.to_numeric(df["Group"], errors="coerce")

        # Filter students based on the criteria
        filtered_df = df[(df[filter_subject] >= min_marks) & (df["Group"] >= group_range[0]) & (df["Group"] <= group_range[1])]

        # Calculate the total marks for the specified subject
        total_marks = filtered_df[subject].sum()

        return {"total_marks": total_marks}
    except Exception as e:
        return {"error": str(e)}


import subprocess
from markdownify import markdownify as md
import fitz  # PyMuPDF

def convert_pdf_to_markdown(file: UploadFile):
    try:
        # Save the uploaded PDF file temporarily
        pdf_path = f"/tmp/{file.filename}"
        with open(pdf_path, "wb") as f:
            f.write(file.file.read())

        # Extract text from the PDF using PyMuPDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()

        # Convert the extracted text to Markdown
        markdown_content = md(text)

        # Save the Markdown content to a temporary file
        markdown_path = pdf_path.replace(".pdf", ".md")
        with open(markdown_path, "w") as md_file:
            md_file.write(markdown_content)

        # Format the Markdown file using Prettier
        subprocess.run(["npx", "-y", "prettier@3.4.2", "--write", markdown_path], check=True)

        # Read the formatted Markdown content
        with open(markdown_path, "r") as formatted_md_file:
            formatted_markdown = formatted_md_file.read()

        return {"formatted_markdown": formatted_markdown}
    except Exception as e:
        return {"error": str(e)}


import pandas as pd
from datetime import datetime
from fastapi import UploadFile

def calculate_total_margin(file: UploadFile, product: str, country: str, time_filter: str):
    try:
        # Save the uploaded Excel file temporarily
        excel_path = f"/tmp/{file.filename}"
        with open(excel_path, "wb") as f:
            f.write(file.file.read())

        # Load the Excel file into a DataFrame
        df = pd.read_excel(excel_path)

        # Trim and normalize strings in Customer Name and Country fields
        df['Customer Name'] = df['Customer Name'].str.strip()
        df['Country'] = df['Country'].str.strip().replace({"USA": "US", "U.S.A": "US"})

        # Standardize date formats
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=False, infer_datetime_format=True)

        # Extract the product name before the slash
        df['Product'] = df['Product'].str.split('/').str[0].str.strip()

        # Clean and convert Sales and Cost fields
        df['Sales'] = df['Sales'].str.replace('USD', '').str.strip().astype(float)
        df['Cost'] = df['Cost'].str.replace('USD', '').str.strip()
        df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
        df['Cost'].fillna(df['Sales'] * 0.5, inplace=True)

        # Filter the data based on the criteria
        time_filter_date = datetime.strptime(time_filter, "%a %b %d %Y %H:%M:%S %Z%z")
        filtered_df = df[(df['Date'] <= time_filter_date) &
                         (df['Product'] == product) &
                         (df['Country'] == country)]

        # Calculate the total margin
        total_sales = filtered_df['Sales'].sum()
        total_cost = filtered_df['Cost'].sum()
        total_margin = (total_sales - total_cost) / total_sales if total_sales > 0 else 0

        return {"total_margin": total_margin}
    except Exception as e:
        return {"error": str(e)}


import gzip
import re
from datetime import datetime
from fastapi import UploadFile

def count_successful_get_requests(file: UploadFile, language: str, day: str, start_time: str, end_time: str):
    try:
        # Save the uploaded GZipped log file temporarily
        gz_path = f"/tmp/{file.filename}"
        with open(gz_path, "wb") as f:
            f.write(file.file.read())

        # Open and read the GZipped file
        with gzip.open(gz_path, "rt", encoding="utf-8") as gz_file:
            logs = gz_file.readlines()

        # Compile regex to parse log entries
        log_pattern = re.compile(
            r'(?P<ip>\S+) (?P<logname>\S+) (?P<user>\S+) \[(?P<time>.+?)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+) "(?P<referer>.*?)" "(?P<user_agent>.*?)" (?P<vhost>\S+) (?P<server>\S+)'
        )

        # Convert start and end times to datetime objects
        start_time_obj = datetime.strptime(start_time, "%H:%M")
        end_time_obj = datetime.strptime(end_time, "%H:%M")

        # Initialize counter for successful GET requests
        successful_get_count = 0

        for log in logs:
            match = log_pattern.match(log)
            if not match:
                continue

            log_data = match.groupdict()

            # Filter by method, status, and URL
            if log_data["method"] != "GET" or not (200 <= int(log_data["status"]) < 300):
                continue

            if not log_data["url"].startswith(f"/{language}/"):
                continue

            # Parse the time and filter by day and time range
            log_time = datetime.strptime(log_data["time"], "%d/%b/%Y:%H:%M:%S %z")
            log_time = log_time.astimezone()  # Convert to local timezone

            if log_time.strftime("%A") != day:
                continue

            if not (start_time_obj.time() <= log_time.time() < end_time_obj.time()):
                continue

            # Increment the counter
            successful_get_count += 1

        return {"successful_get_requests": successful_get_count}
    except Exception as e:
        return {"error": str(e)}

import gzip
from collections import defaultdict

def top_ip_data_consumer(file: UploadFile, language: str, date: str):
    try:
        # Save the uploaded GZipped log file temporarily
        gz_path = f"/tmp/{file.filename}"
        with open(gz_path, "wb") as f:
            f.write(file.file.read())

        # Open and read the GZipped file
        with gzip.open(gz_path, "rt", encoding="utf-8") as gz_file:
            logs = gz_file.readlines()

        # Compile regex to parse log entries
        log_pattern = re.compile(
            r'(?P<ip>\S+) (?P<logname>\S+) (?P<user>\S+) \[(?P<time>.+?)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+) "(?P<referer>.*?)" "(?P<user_agent>.*?)" (?P<vhost>\S+) (?P<server>\S+)'
        )

        # Initialize a dictionary to aggregate data by IP
        ip_data = defaultdict(int)

        for log in logs:
            match = log_pattern.match(log)
            if not match:
                continue

            log_data = match.groupdict()

            # Filter by URL and date
            if not log_data["url"].startswith(f"/{language}/"):
                continue

            log_time = datetime.strptime(log_data["time"], "%d/%b/%Y:%H:%M:%S %z")
            log_time = log_time.astimezone()  # Convert to local timezone

            if log_time.strftime("%Y-%m-%d") != date:
                continue

            # Aggregate the size by IP
            size = int(log_data["size"]) if log_data["size"].isdigit() else 0
            ip_data[log_data["ip"]] += size

        # Identify the top data consumer
        top_ip = max(ip_data, key=ip_data.get, default=None)
        top_bytes = ip_data[top_ip] if top_ip else 0

        return {"top_ip": top_ip, "total_bytes": top_bytes}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/outline")
def create_country_outline_api(country: str = Query(..., description="The name of the country")):
    try:
        # Construct the Wikipedia URL for the country
        wikipedia_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"

        # Fetch the Wikipedia page content
        response = requests.get(wikipedia_url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all headings (H1 to H6) from the page
        headings = []
        for level in range(1, 7):
            for heading in soup.find_all(f'h{level}'):
                headings.append((level, heading.text.strip()))

        # Generate the Markdown outline
        markdown_outline = ["## Contents", f"# {country}"]
        for level, text in headings:
            markdown_outline.append(f"{'#' * level} {text}")

        return {"markdown_outline": "\n".join(markdown_outline), "endpoint": "http://127.0.0.1:8000/api/outline"}
    except Exception as e:
        return {"error": str(e)}

import pandas as pd
from fastapi import UploadFile
from fuzzywuzzy import process
import json

def aggregate_sales_by_city(file: UploadFile, product: str, min_units: int, city: str):
    try:
        # Save the uploaded JSON file temporarily
        json_path = f"/tmp/{file.filename}"
        with open(json_path, "wb") as f:
            f.write(file.file.read())

        # Load the JSON file into a DataFrame
        with open(json_path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        # Normalize city names using phonetic clustering
        unique_cities = df['city'].unique()
        city_mapping = {}
        for unique_city in unique_cities:
            best_match = process.extractOne(unique_city, unique_cities)[0]
            city_mapping[unique_city] = best_match

        df['city'] = df['city'].map(city_mapping)

        # Filter the dataset based on the criteria
        filtered_df = df[(df['product'] == product) & (df['sales'] >= min_units)]

        # Aggregate sales by city
        aggregated_sales = filtered_df.groupby('city')['sales'].sum()

        # Get the sales for the specified city
        total_sales = aggregated_sales.get(city, 0)

        return {"total_sales": total_sales}
    except Exception as e:
        return {"error": str(e)}


import json

def calculate_total_sales_from_jsonl(file: UploadFile):
    try:
        # Save the uploaded JSONL file temporarily
        jsonl_path = f"/tmp/{file.filename}"
        with open(jsonl_path, "wb") as f:
            f.write(file.file.read())

        # Read and parse the JSONL file
        total_sales = 0
        with open(jsonl_path, "r") as f:
            for line in f:
                try:
                    # Attempt to parse the JSON line
                    data = json.loads(line.strip())
                except json.JSONDecodeError:
                    # If parsing fails, try to fix the line
                    fixed_line = line.strip()
                    if not fixed_line.endswith('}'):
                        fixed_line += '}'
                    if not fixed_line.startswith('{'):
                        fixed_line = '{' + fixed_line
                    data = json.loads(fixed_line)

                # Add the sales value if it exists
                total_sales += data.get("sales", 0)

        return {"total_sales": total_sales}
    except Exception as e:
        return {"error": str(e)}


import json

def count_key_occurrences(file: UploadFile, key: str):
    try:
        # Save the uploaded JSON file temporarily
        json_path = f"/tmp/{file.filename}"
        with open(json_path, "wb") as f:
            f.write(file.file.read())

        # Load the JSON file
        with open(json_path, "r") as f:
            data = json.load(f)

        # Recursive function to count key occurrences
        def count_key(data, key):
            if isinstance(data, dict):
                return sum((1 if k == key else 0) + count_key(v, key) for k, v in data.items())
            elif isinstance(data, list):
                return sum(count_key(item, key) for item in data)
            return 0

        # Count the occurrences of the key
        total_count = count_key(data, key)

        return {"key_occurrences": total_count}
    except Exception as e:
        return {"error": str(e)}

def generate_duckdb_query(date: str, time: str, stars: int):
    try:
        # Combine date and time into a single timestamp
        timestamp = f"{date}T{time}"

        # Generate the DuckDB SQL query
        query = f"""
        SELECT post_id
        FROM (
            SELECT post_id, json_extract(comments, '$[*].stars.useful') AS useful_stars
            FROM social_media 
            WHERE timestamp > '{timestamp}'
        ) 
        WHERE EXISTS (
            SELECT 1 
            FROM UNNEST(useful_stars) AS t(value)
            WHERE CAST(value AS INTEGER) >= {stars}
        )
        ORDER BY post_id;
        """

        return {"query": query}
    except Exception as e:
        return {"error": str(e)}

import base64
from PIL import Image
import numpy as np

def reconstruct_image(image_path: str, mapping: list):
    try:
        # Open the scrambled image
        scrambled_image = Image.open(image_path)

        # Define the size of each piece
        piece_size = scrambled_image.width // 5

        # Create a blank image for the reconstructed image
        reconstructed_image = Image.new('RGB', (scrambled_image.width, scrambled_image.height))

        # Reconstruct the image based on the mapping
        for original_row, original_col, scrambled_row, scrambled_col in mapping:
            # Extract the piece from the scrambled image
            left = scrambled_col * piece_size
            upper = scrambled_row * piece_size
            right = left + piece_size
            lower = upper + piece_size
            piece = scrambled_image.crop((left, upper, right, lower))

            # Paste the piece into the reconstructed image
            left = original_col * piece_size
            upper = original_row * piece_size
            reconstructed_image.paste(piece, (left, upper))

        # Save the reconstructed image to a temporary path
        reconstructed_path = "/tmp/reconstructed_image.png"
        reconstructed_image.save(reconstructed_path)

        # Convert the reconstructed image to base64 encoding
        with open(reconstructed_path, "rb") as img_file:
            base64_encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

        return {"base64_encoded_image": base64_encoded_image}
    except Exception as e:
        return {"error": str(e)}

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["OPTIONS", "POST"],  # Allow OPTIONS and POST methods
    allow_headers=["*"],  # Allow all headers
)

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function descriptions and mapping
functions_dict = {}
function_descriptions = []

# Main /api endpoint
@app.post("/api")
def handle_api_request(question: str = Form(...), file: UploadFile = File(None)):
    try:
        # Calculate similarity between the question and function descriptions using embeddings
        question_embedding = model.encode(question)
        function_embeddings = model.encode(function_descriptions)
        cosine_similarities = cosine_similarity([question_embedding], function_embeddings).flatten()
        most_similar_function_index = cosine_similarities.argmax()
        most_similar_function = list(functions_dict.values())[most_similar_function_index]

        # Call the most similar function
        if file:
            return most_similar_function(file=file, question=question)
        else:
            return most_similar_function(question=question)
    except Exception as e:
        return {"error": str(e)}

# Register functions
functions_dict.update({
    "compute_similarity": lambda **kwargs: {"api_link": "http://127.0.0.1:8000/similarity"},
    "execute_query": lambda **kwargs: {"api_link": "http://127.0.0.1:8000/execute"}
})

function_descriptions.extend([
    "Compute similarity between documents and a query",
    "Execute a query and return the result"
])


