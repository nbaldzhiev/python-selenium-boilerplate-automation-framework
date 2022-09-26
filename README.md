# Core Selenium Boilerplate Project (Python)

The repository contains a boilerplate project for a core Selenium framework with Python. "Core" would mean that the project supports the most fundamental 
parts of a UI framework with Selenium:
* cross-browser support:
  - Chrome;
  - Firefox;
  - Edge.
* various UI elements support:
  - `Input`;
  - `Checkbox`;
  - `Dropdown` - single-select and multi-select;
  - `Table`;
  - `Collection` - a collection of elements with a common locator.

The idea is to make it easier for a given team to bootstrap its UI test automation effort. The framework aims to be generic enough and can be adjusted according to a specific product under test.

## Tech stack
* Python 3.7+
* Selenium 4.4.3

Please refer to installing the requirements in the file `requirements.txt` in a Python virtual environment in order to ensure that all required packages are present.

## Other

The project uses the following packages for code style formatting:
* isort
* black
* pylint
