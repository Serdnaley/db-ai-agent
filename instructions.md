# Project Instructions: Minimal File Structure with Vue.js and Python Backend

## Overview

To create the simplest version of your data analysis and visualization tool, we'll set up a minimal project using Vue.js for the client side and Python for the backend. The goal is to keep the number of files as low as possible while maintaining functionality.

## Project Structure

Here's the minimal file structure:

```
project/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── app.js
└── requirements.txt
```

- **Total Files**: 4 (excluding directories)

## Instructions

### 1. Backend Setup (`app.py`)

We'll use **Flask** for a simple backend server.

```python
# app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import io
import base64

app = Flask(__name__)

# Database connection parameters
DB_HOST = 'your_db_host'
DB_NAME = 'your_db_name'
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data_prompt = request.json.get('data_prompt')
    viz_prompt = request.json.get('viz_prompt')

    # Log the request with a simple query ID
    print(f"[Query ID: {id(request)}] Received data_prompt and viz_prompt")

    try:
        # Establish database connection
        conn = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        # Execute SQL query from data_prompt
        df = pd.read_sql_query(data_prompt, conn)
        conn.close()

        # Generate visualization
        plt.figure()
        plot_kind = viz_prompt.lower()
        df.plot(kind=plot_kind)
        plt.tight_layout()

        # Save plot to a PNG image in memory
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_base64 = base64.b64encode(img.getvalue()).decode()

        # Return the image as a base64 string
        return jsonify({'plot_url': f'data:image/png;base64,{plot_base64}'})

    except Exception as e:
        print(f"[Query ID: {id(request)}] Error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

**Notes:**

- Replace `'your_db_host'`, `'your_db_name'`, `'your_db_user'`, and `'your_db_password'` with your actual PostgreSQL database credentials.
- This script uses minimal error handling and logs to `stdout` with a simple query ID.

### 2. Frontend Template (`templates/index.html`)

The HTML template serves the Vue.js application.

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Data Visualization Tool</title>
</head>
<body>
    <div id="app">
        <h2>Data Analysis and Visualization</h2>
        <div>
            <label>Data Retrieval Prompt:</label><br>
            <textarea v-model="dataPrompt" rows="4" cols="50"></textarea>
        </div>
        <div>
            <label>Visualization Prompt:</label><br>
            <input v-model="vizPrompt" placeholder="e.g., bar, line, scatter">
        </div>
        <button @click="submitPrompts">Generate Visualization</button>

        <div v-if="plotUrl">
            <h3>Result:</h3>
            <img :src="plotUrl" alt="Visualization Result">
        </div>

        <div v-if="errorMessage" style="color: red;">
            <p>Error: {{ errorMessage }}</p>
        </div>
    </div>

    <!-- Include Vue.js from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
    <!-- Include the Vue.js app script -->
    <script src="{{ url_for('static', filename='app.js') }}"></script>
</body>
</html>
```

**Notes:**

- Uses Vue.js via CDN to avoid additional files.
- Minimal styling and structure for simplicity.

### 3. Frontend Script (`static/app.js`)

The Vue.js application logic.

```javascript
// static/app.js
new Vue({
    el: '#app',
    data: {
        dataPrompt: '',
        vizPrompt: '',
        plotUrl: '',
        errorMessage: ''
    },
    methods: {
        submitPrompts() {
            this.errorMessage = '';
            this.plotUrl = '';
            fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data_prompt: this.dataPrompt,
                    viz_prompt: this.vizPrompt
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.plot_url) {
                    this.plotUrl = data.plot_url;
                } else if (data.error) {
                    this.errorMessage = data.error;
                }
            })
            .catch(error => {
                this.errorMessage = 'An error occurred while processing your request.';
                console.error('Error:', error);
            });
        }
    }
});
```

**Notes:**

- Handles the submission of prompts and displays the resulting image or error message.
- Uses the Fetch API to send a POST request to the backend.

### 4. Dependencies (`requirements.txt`)

List of required Python packages.

```
flask
pandas
matplotlib
psycopg2-binary
```

**Notes:**

- `psycopg2-binary` is used for PostgreSQL connectivity.
- Ensure these packages are installed in your Python environment.

## Setup Instructions

### Step 1: Install Python Dependencies

Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Configure Database Connection

Edit `app.py` and replace the database connection parameters with your credentials:

```python
# In app.py
DB_HOST = 'your_db_host'
DB_NAME = 'your_db_name'
DB_USER = 'your_db_user'
DB_PASSWORD = 'your_db_password'
```

### Step 3: Run the Application

Start the Flask server by executing:

```bash
python app.py
```

### Step 4: Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

## Usage Instructions

1. **Data Retrieval Prompt**: Enter your SQL query directly. For simplicity, we assume the prompt is a valid SQL query.

   - Example:
     ```sql
     SELECT * FROM sales LIMIT 10;
     ```

2. **Visualization Prompt**: Specify the type of plot you want.

   - Options include: `line`, `bar`, `scatter`, `hist`, etc.
   - Example:
     ```
     bar
     ```

3. **Generate Visualization**: Click the **"Generate Visualization"** button.

4. **View Result**: The resulting plot will be displayed below the button.

## Simplifications Made

- **Single-Page Application**: The entire frontend is served from a single HTML file with an embedded Vue.js app.
- **Minimal Backend Logic**: The backend consists of one Python file (`app.py`) handling all server-side operations.
- **Assumed Valid Input**: The application assumes that users provide valid SQL queries and visualization types.
- **No Additional Configuration Files**: Aside from `requirements.txt`, there are no extra configuration files.

## Logging and Error Handling

- **Logging**: All logs are printed to `stdout` with a simple query ID based on the request object's ID.
- **Error Handling**: Errors are caught and returned to the frontend to be displayed to the user.

## Important Considerations

- **Security**: Executing raw SQL queries from user input can lead to SQL injection attacks. Since this is an internal, trusted environment and a concept project, we have not implemented input sanitization. **Do not use this approach in a production environment without proper input validation and sanitization.**
- **Error Messages**: For simplicity, error messages are directly returned to the user. In a real-world scenario, you might want to handle errors differently to avoid exposing sensitive information.
- **Dependencies**: Ensure that all dependencies are properly installed and compatible with your system.

## Conclusion

By following these instructions, you will have a minimal, functional prototype of your data analysis and visualization tool with as few files as possible. This setup allows you to focus on the core concept while providing a foundation that can be expanded in the future if needed.