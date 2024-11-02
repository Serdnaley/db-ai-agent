# Technical Task: Data Analysis and Visualization Tool Concept

## Overview

Develop a simple, standalone Python application that allows technically proficient users (engineers and analysts) to retrieve data from PostgreSQL databases based on text prompts and generate visualizations using Python libraries like Matplotlib. The application focuses on one-time data retrieval and visualization without the need for complex user management or security features.

## Objectives

- **User Prompt Interaction**: Accept text-based user prompts specifying data retrieval and visualization requirements.
- **Data Retrieval**: Query data from PostgreSQL databases dynamically based on user prompts.
- **Data Processing**: Use Python libraries to process and combine data, including joins and aggregations.
- **Visualization**: Generate static images of data visualizations as specified by the user.
- **Simplicity**: Keep the application as straightforward as possible, focusing on core functionalities.

## Functional Requirements

### 1. User Prompt Input

- **Input Method**: Users provide prompts as plain text inputs.
- **Prompt Structure**:
  - **Data Retrieval Instructions**: Specify tables, fields, conditions, and any necessary joins or aggregations.
  - **Visualization Instructions**: Indicate the type of visualization (e.g., line chart, bar graph) and any specific formatting or data to highlight.
- **Example Prompt**:
  ```
  Data Retrieval: Select sales data from the last quarter joining tables 'sales' and 'customers' on 'customer_id'.
  Visualization: Create a bar chart showing total sales per region.
  ```

### 2. Data Retrieval

- **Database Connection**:
  - Connect to one or more PostgreSQL databases using provided connection details.
  - Capture the Data Definition Language (DDL) to understand the database schema.
- **Query Execution**:
  - Parse the user's data retrieval instructions to form SQL queries.
  - Support complex queries involving joins, aggregations, and conditions.
  - Handle dynamic schemas without hardcoding table or column names.
- **Data Handling**:
  - Fetch data and load it into Python data structures (e.g., Pandas DataFrames).

### 3. Data Processing

- **Libraries**: Utilize Pandas or similar libraries for data manipulation.
- **Data Merging**:
  - Combine data from different sources or tables as required.
  - Perform necessary data transformations based on the user's prompt.
- **Aggregations and Calculations**:
  - Compute sums, averages, counts, or other statistical measures as specified.

### 4. Data Visualization

- **Visualization Tools**: Use Matplotlib for generating charts and graphs.
- **Supported Visualizations**:
  - Bar charts, line graphs, scatter plots, pie charts, etc.
- **Customization**:
  - Basic styling and formatting as per default settings.
  - Include numerical data labels if specified.
- **Output**:
  - Generate static images of the visualizations.
  - No interactive features are required.

### 5. Output Delivery

- **Display**:
  - Show the generated images within the application interface (e.g., pop-up window or inline display).
- **Saving Images**:
  - Users can save images using native tools (e.g., right-click to save) or take screenshots.
- **No Additional Features**:
  - No need for export functions, reports, or data downloads.

### 6. Logging and Error Handling

- **Logging**:
  - Write logs to stdout with a prefix of a query ID for easy tracking.
  - Include timestamps and brief descriptions of actions performed.
- **Error Handling**:
  - Display simple error messages if a query fails or invalid input is provided.
  - No need for advanced error recovery mechanisms.

### 7. Authentication (Optional)

- **Simple Authentication**:
  - If necessary, implement a basic authentication mechanism (e.g., a hardcoded password).
  - No user management or role-based access control is required.

## Non-Functional Requirements

- **Performance**:
  - Performance optimization is not a priority.
  - Acceptable to have delays due to data size or processing time.
- **Security**:
  - Security measures are minimal due to the internal and conceptual nature of the project.
  - Assume a trusted environment.
- **Scalability**:
  - Designed for one-time, manual runs per project.
  - No need to handle concurrent users or large-scale deployments.
- **Maintainability**:
  - Code should be clean and well-documented for ease of understanding.
  - Use straightforward programming practices without over-engineering.

## Technologies and Tools

- **Programming Language**: Python (latest stable version).
- **Database**: PostgreSQL.
- **Python Libraries**:
  - **Database Connectivity**: `psycopg2` or `SQLAlchemy`.
  - **Data Manipulation**: `Pandas`.
  - **Visualization**: `Matplotlib`.
- **Execution Environment**:
  - Run locally on a user's machine.
  - No need for containerization or virtual environments unless already in use.

## Project Workflow

1. **Setup**:
   - Configure database connection parameters.
   - Install necessary Python libraries.
2. **User Input**:
   - Prompt the user for data retrieval and visualization instructions.
3. **Data Retrieval**:
   - Parse the input and construct SQL queries.
   - Execute queries and fetch data.
4. **Data Processing**:
   - Load data into Pandas DataFrames.
   - Perform any joins, aggregations, or transformations.
5. **Visualization**:
   - Generate the specified charts or graphs using Matplotlib.
   - Display the visualization to the user.
6. **Output and Logging**:
   - Provide options for the user to save the visualization.
   - Log the process with query IDs and timestamps.

## Assumptions

- **Users**:
  - Are familiar with technical concepts and comfortable with text-based interfaces.
  - Understand the database schema or have access to schema information.
- **Data**:
  - Is accessible and the user has necessary permissions to query it.
  - Can change frequently; the application retrieves the most recent data upon each run.
- **Environment**:
  - The application runs in a secure, internal environment where security risks are minimal.
  - Dependencies are installed and compatible with the system.

## Limitations

- **User Interface**:
  - No graphical user interface (GUI) beyond text prompts and image display.
  - No web interface or browser-based interaction.
- **Error Handling**:
  - Limited to basic notifications; does not provide detailed diagnostics.
- **Customization**:
  - Visualization customization is minimal; advanced styling is not supported.
- **Extensibility**:
  - The application is a concept prototype and may not accommodate future feature expansions without additional development.

## Deliverables

- **Source Code**:
  - Python script(s) implementing the described functionalities.
  - Well-commented code for readability.
- **Documentation**:
  - Instructions on how to set up and run the application.
  - Examples of user prompts and expected outputs.
- **Sample Data and Prompts**:
  - Optional sample datasets or database schemas for testing.
  - Example prompts to demonstrate application capabilities.

## Conclusion

This technical task outlines the development of a simplified data analysis and visualization tool tailored for internal use by engineers and analysts. The focus is on enabling users to quickly retrieve and visualize data from PostgreSQL databases using straightforward Python scripts without unnecessary complexity.