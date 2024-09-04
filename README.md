# Rally Integration Script and Web Application

## Overview

This project consists of a Python script for integrating with Rally (now part of Broadcom) and a Flask web application that provides a user interface for uploading Excel files and creating user stories and tasks in Rally.

## Requirements

- Python 3.6+
- `pyral` library
- `pandas` library
- `numpy` library
- `flask` library
- Access to a Rally account with appropriate permissions

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Install the required libraries:
   ```
   pip install pyral pandas numpy openpyxl flask
   ```
3. Place the `rally_integration.py` and `app.py` files in your project directory.

## Obtaining a Rally API Key

To use this integration, you'll need a Rally API Key. Here's how to obtain one:

1. Log in to your Rally account.
2. Navigate to your user settings.
3. Look for a tab or section labeled "API Keys".
4. Click on "Create"
5. Give your API key a name (e.g., "Rally Integration Script").
6. Copy the generated API key and store it securely. You'll need this for the script.

Note: API keys are sensitive information. Never share your API key.

## Flask Web Application

The Flask application provides a web interface for uploading Excel files and creating user stories and tasks in Rally.

### Setting Up the Flask App

1. Ensure you have the `app.py` file in your project directory.
2. Create a `templates` folder in the same directory.
3. Create the following HTML templates in the `templates` folder:
   - `home.html`: The main page with the file upload form
   - `success.html`: A page to show when the operation is successful
   - `failure.html`: A page to show when an error occurs

### Launching the Flask App

1. Open a terminal or command prompt.
2. Navigate to the directory containing `app.py`.
3. Run the following command:
   ```
   python app.py
   ```
4. The Flask development server will start, typically on `http://127.0.0.1:5000/`.
5. Open this URL in your web browser to access the application.

### Using the Web Interface

1. On the home page, you'll see a form to input Rally credentials and upload an Excel file.
2. Fill in the following fields:
   - API Key: Your Rally API key
   - Username: Your Rally username
   - Workspace: The name of your Rally workspace
   - Project: The name of your Rally project
3. Upload your prepared Excel file.
4. Click the Submit button to process the file and create user stories and tasks in Rally.

## Excel File Structure

Prepare your Excel file with the following columns:

| Column | Name | Description |
|--------|------|-------------|
| A | User Story or Task | Must contain either "User Story" or "Task" |
| B | Name | Name of the user story or task |
| C | Description | Description (can be left blank for tasks) |
| D | Plan Estimate | For user stories (can be left blank for tasks) |
| E | Todo Hours | For tasks (can be left blank for user stories) |
| F | Estimate Hours | For tasks (can be left blank for user stories) |
| G | Release | For user stories (can be left blank for tasks) |
| H | Iteration | For user stories (can be left blank for tasks) |
| I | Development End Date | For user stories, in MM/DD/YYYY format (can be left blank for tasks) |
| J | Owner | Username for both user stories and tasks |

## Sample Excel File Content

| User Story or Task | Name | Description | Plan Estimate | Todo Hours | Estimate Hours | Release | Iteration | Development End Date | Owner |
|--------------------|------|-------------|---------------|------------|----------------|---------|-----------|----------------------|-------|
| User Story | Implement login | Create login functionality | 5 | | | Release 1 | Sprint 1 | 12/31/2024 | john.doe@company.com |
| Task | Design UI | | | 3 | 3 | | | | jane.smith@company.com |
| Task | Implement backend | | | 5 | 5 | | | | john.doe@company.com |
| User Story | Add dashboard | Create user dashboard | 8 | | | Release 1 | Sprint 2 | 01/15/2025 | jane.smith@company.com |
| Task | Design layout | | | 4 | 4 | | | | designer.user@company.com |
| Task | Implement widgets | | | 6 | 6 | | | | developer.user@company.com |

## Important Notes

1. Ensure that the usernames in the 'Owner' column exist in your Rally instance. If a username is not found, the script will use the default username provided when calling the function.

2. The 'User Story or Task' column must contain either "User Story" or "Task" (case-insensitive).

3. Tasks must immediately follow their associated user story in the Excel file.

4. If a task's owner is left blank, it will inherit the owner from its parent user story.

5. The Release and Iteration names must match exactly with those in your Rally instance.

6. The Development End Date should be in MM/DD/YYYY format.

7. Numeric fields (Plan Estimate, Todo Hours, Estimate Hours) can be left blank if not applicable.

8. Make sure that the name of the "Release" and "Iteration" match what you have in your rally project.

## Error Handling

If the script encounters an error, it will display an error message on the failure page. Common errors include:
- Missing required columns in the Excel file
- Invalid values in the 'User Story or Task' column
- Tasks defined before a user story
- Failure to find specified Releases or Iterations in Rally

## Security Notes

1. The Flask development server is not suitable for production use. For production deployment, use a production-grade WSGI server like Gunicorn or uWSGI.
2. Implement proper authentication and authorization in the Flask app before deploying it in a production environment.
3. Use HTTPS to encrypt data in transit, especially when handling API keys and other sensitive information.
4. Consider using environment variables or a secure secrets management solution to handle the Rally API key and other sensitive configuration data.

## Support

For any issues or questions, please contact your Rally administrator or the script maintainer.

