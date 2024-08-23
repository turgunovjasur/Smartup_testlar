# SmartUp Online Test Automation

This project has automated tests for the Startup online platform. The tests cover the input process and base function.

## Requirements

- Python 3.x
- Selenium WebDriver
- pytest
- Chrome browser (versiya: 127.0.6533.72)

## Installation

1. Download the project files.
2. Install the required libraries: pip install selenium pytest
3. Download ChromeDriver.

## Running Tests

Use the following commands to run the tests:

1. To run all tests:
- pytest
2. To run test files: 
- pytest
3. To obtain a report in Allure
- allure serve reports/allure_results 

## Test Details

This test includes the following steps:
1. Logging in
- checks whether it has successfully passed the login page

2. Base function
- common functions used in all testcases

## Important Notes

- Ensure you have a stable internet connection before running the tests.
- Remember to adjust Chrome Driver to your computer's settings.
- Test results will be displayed in the console window.

## Test Structure

The tests use a Page Object Model (POM) design pattern, which separates the page structure from the tests themselves. This makes the tests more maintainable and easier to read.

## Troubleshooting

If you encounter any issues:
1. Check that all dependencies are correctly installed.
2. Ensure the ChromeDriver version matches your Chrome browser version.
3. Verify that the URLs and XPaths in the tests are still valid for the current version of the SmartUp Online platform.