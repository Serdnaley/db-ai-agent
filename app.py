import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import io
import base64
from dotenv import load_dotenv
import os
from openai import OpenAI
import ast
import traceback
import signal
import sys

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Validate required environment variables
required_env_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'OPENAI_API_KEY', 'SERVER_HOST', 'SERVER_PORT']
missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_env_vars:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing_env_vars)}")

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def execute_sql_query(query):
    """Executes a SQL query and returns a Pandas DataFrame."""
    # Establish database connection
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    try:
        # Use parameterized queries to prevent SQL injection
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def get_table_schema():
    """Get the schema information for all tables in the database."""
    try:
        # Query to get table schemas
        schema_query = """
        SELECT 
            t.table_name,
            array_agg(c.column_name || ' ' || c.data_type) as columns
        FROM 
            information_schema.tables t
            JOIN information_schema.columns c ON t.table_name = c.table_name
        WHERE 
            t.table_schema = 'public'
            AND t.table_type = 'BASE TABLE'
        GROUP BY 
            t.table_name;
        """
        df = execute_sql_query(schema_query)
        
        # Format the schema information
        schema_info = []
        for _, row in df.iterrows():
            schema_info.append(f"Table: {row['table_name']}")
            schema_info.append("Columns: " + ", ".join(row['columns']))
            schema_info.append("")
        
        return "\n".join(schema_info)
    except Exception as e:
        print(f"Error getting schema: {e}")
        return "Schema information unavailable"

def generate_code_from_prompt(prompt):
    """Uses OpenAI API to generate Python code based on the natural language prompt."""
    # Get database schema
    schema_info = get_table_schema()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are a helpful assistant that writes Python code to query a PostgreSQL database and generate a matplotlib visualization based on the user's request.

Write only the Python code, without any markdown formatting, code block indicators, or explanations. Use the execute_sql_query function for database queries."""},
            {"role": "user", "content": f"""
Database Schema:
{schema_info}

Constraints:
- Use the execute_sql_query(query) function for database queries
- Store the query result in a variable named 'df'
- Generate a matplotlib plot using plt.figure() and df.plot()
- Set appropriate labels using plt.xlabel(), plt.ylabel(), and plt.title()
- Use plt.tight_layout() at the end
- Do not include any calls to plt.show() or plt.savefig()
- Do not establish new database connections
- Do not include markdown formatting or code block indicators
- Do not redefine database connection parameters
- Only use tables and columns that exist in the schema
- Use appropriate data types for the columns
- Handle potential NULL values in the data

Example format:
df = execute_sql_query("YOUR QUERY HERE")
plt.figure(figsize=(10, 6))
df.plot(kind='TYPE', ...)
plt.title('TITLE')
plt.xlabel('X LABEL')
plt.ylabel('Y LABEL')
plt.tight_layout()

User request: "{prompt}"
"""}
        ],
        temperature=0
    )
    
    # Extract the generated code from the response and clean it
    code = response.choices[0].message.content.strip()
    
    # Remove markdown code block indicators if present
    if code.startswith('```python'):
        code = code.split('\n', 1)[1]
    if code.endswith('```'):
        code = code.rsplit('\n', 1)[0]
    
    # Remove any remaining markdown formatting
    code = code.replace('```', '')
    
    return code.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt')

    # Log the request with a simple query ID
    query_id = id(request)
    print(f"[Query ID: {query_id}] Received natural language prompt")

    try:
        # Generate code from the natural language prompt
        code = generate_code_from_prompt(prompt)

        # Log the generated code (for debugging, remove in production)
        print(f"[Query ID: {query_id}] Generated code:\n{code}")

        # Create a safe globals dictionary with necessary functions and modules
        safe_globals = {
            'pd': pd,
            'plt': plt,
            'execute_sql_query': execute_sql_query,
            'DB_HOST': DB_HOST,
            'DB_PORT': DB_PORT,
            'DB_NAME': DB_NAME,
            'DB_USER': DB_USER,
            'DB_PASSWORD': DB_PASSWORD,
            '__builtins__': {
                'len': len,
                'range': range,
                'dict': dict,
                'list': list,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'tuple': tuple,
                'map': map,
                'zip': zip,
                'min': min,
                'max': max,
                'sum': sum,
                'print': print,
                'type': type
            }
        }

        # Create a local namespace dictionary
        local_namespace = {}

        # Clear any existing plots
        plt.clf()
        plt.close('all')

        # Execute the generated code safely
        exec(code, safe_globals, local_namespace)

        # Ensure we have a DataFrame named 'df' in the local namespace
        if 'df' not in local_namespace:
            raise ValueError("The code did not create a DataFrame named 'df'")

        # Ensure a plot was created
        if len(plt.get_fignums()) == 0:
            # If no plot exists, create one from the DataFrame
            df = local_namespace['df']
            if len(df.columns) >= 2:
                df.plot(kind='bar')
            else:
                df.plot(kind='bar', y=df.columns[0])
            plt.title('Generated Plot')
            plt.tight_layout()

        # Save plot to a PNG image in memory
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', dpi=300, pad_inches=0.1)
        img.seek(0)
        plot_base64 = base64.b64encode(img.getvalue()).decode()

        # Clear the current figure to prevent overlap in future plots
        plt.clf()
        plt.close('all')

        # Return the image as a base64 string
        return jsonify({'plot_url': f'data:image/png;base64,{plot_base64}'})

    except Exception as e:
        error_message = ''.join(traceback.format_exception_only(type(e), e)).strip()
        print(f"[Query ID: {query_id}] Error: {error_message}")
        plt.clf()  # Clean up any partial plots
        plt.close('all')
        return jsonify({'error': str(error_message)}), 400

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    # Clean up any remaining connections
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
    try:
        app.run(
            host=SERVER_HOST,
            port=SERVER_PORT,
            debug=True
        )
    finally:
        # Cleanup code here
        print('Cleaning up...')