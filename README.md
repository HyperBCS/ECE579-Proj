# ECE579-Proj
Final project for ECE 579

# Installation

**Requirements**

- Python 3
- Pip3
- Data from http://files.pushshift.io/reddit/submissions/


**Step 1: Downloading Data**
From the link provided above download any number of submission archives and extract them to a folder named "input" in the root directory of the project. This is the folder the program will read from.

**Step 2: Installing requirements**

Linux:
To install python packages. From the "ECE579-Proj" directory type
```sudo pip3 install virtualenv``` to install the virtual evniornment binaries

Next run ```virtualenv -p python3 venv``` to setup the virtualenv for this project

```source venv/bin/activate``` To setup the enviornment variables and setup your python session


```pip3 install -r requirements.txt``` To install the packages
# Running The program
From the project directory
```python sent-map.py``` to start the analysis. This will load the reddit data from a folder called "input" in the root directory of the project
