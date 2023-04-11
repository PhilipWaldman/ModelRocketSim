# Waldman Rocket Program (WARP)

WARP, short for **Wa**ldman **R**ocket **P**rogram, is a model rocket simulator created by Philip Waldman.

## Installation

The official guide to create virtual python environments can be
found [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). The following steps
are based off of that guide.

### Windows

1. Open command prompt and navigate to this folder using `cd "this folder's location"`.
2. Makes sure that you have the latest version of pip using `py -m pip install --upgrade pip`.
3. Install virtualenv: `py -m pip install --user virtualenv`.
4. Create a virtual environment: `py -m venv warp_env`.
5. Activate the virtual environment: `.\warp_env\Scripts\activate`.
6. Install the required packages: `pip install -r requirements.txt`.
7. Run the tool: `py index.py`.
8. Open a web browser and go to the URL that is mentioned on the first line after the tool is run.
9. Now the tool can be used.
10. In command prompt, press CTRL-C to stop the tool.
11. When done, leave the virtual environment: `deactivate`.

### Linux and macOS

1. Open the terminal and navigate to this folder.
2. Makes sure that you have the latest version of pip using `python3 -m pip install --user --upgrade pip`.
3. Install virtualenv: `python3 -m pip install --user virtualenv`.
4. Create a virtual environment: `python3 -m venv warp_env`.
5. Activate the virtual environment: `source env/bin/activate`.
6. Install the required packages: `pip install -r requirements.txt`.
7. Run the tool: `python3 index.py`.
8. Open a web browser and go to the URL that is mentioned on the first line after the tool is run.
9. Now the tool can be used.
10. In the terminal, press CTRL-C to stop the tool.
11. When done, leave the virtual environment: `deactivate`.

## License

[MIT](https://choosealicense.com/licenses/mit/)
