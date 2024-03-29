# For Developers

If you are interested in contributing to the Commit Tracker project or wish to add new features, please follow the steps below to set up your development environment.

## Installing for Development

To set up your development environment for Commit Tracker, execute the following commands. This will install all necessary development dependencies, including new tools and libraries introduced for handling data visualization and Git repository analysis.

git clone https://github.com/andrecosta99/ct-final.git
cd ct-final
python -m venv env
# On Unix or MacOS
source env/bin/activate
# On Windows
.\env\Scripts\activate
pip install -e .
pre-commit install

Ensure all dependencies are up to date by reviewing the `requirements.txt` file or any other dependency management file used by the project.

## Running Tests

Commit Tracker includes a suite of tests to ensure the quality and functionality of the code. To run these tests, use the following command:

pytest

To generate a coverage report and see which parts of your code are covered by tests, use:

pytest --cov=committracker --cov-report=html

This will create a coverage report in the `htmlcov` directory, which you can open with a web browser.

## Contributing Guidelines

Please review the `CONTRIBUTING.md` file for detailed instructions on how to contribute to the project, including coding standards, pull request processes, and guidelines for writing tests and documentation.

For documentation changes or additions, ensure you are familiar with MkDocs and follow the project's standards for documentation structure and formatting.
