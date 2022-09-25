Install dependencies:
    https://flask.palletsprojects.com/en/2.2.x/installation/
    https://pypi.org/project/requests/
    https://docs.pytest.org/en/7.1.x/getting-started.html
    https://requests-mock.readthedocs.io/en/latest/overview.html#installation

Run from CLI: 
    Navigate to the project directory / use the terminal in IntelliJ
    python -m flask --app flaskr run

IntelliJ:
    Create a new Python configuration. Leave script empty. Set Parameters to "-m flask --app flaskr/server run". Set Working Directory to your project's directory.
    For tests repeat the same process but set Parameters to "-m pytest".
    