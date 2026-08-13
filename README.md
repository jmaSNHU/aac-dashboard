![AAC Outcomes Dashboard](https://jmasnhu.github.io/images/aac-dashboard.jpg)

# aac-dashboard
Enhancement for CS-340's AAC Outcomes Dashboard. Replaces the original MongoDB database with SQLite and normalizes the Austin Animal Center's outcomes dataset.


## Getting Started

To run the code, you must first activate the Python virtual environment included in the repository:

```source myenv/bin/activate```

## Creating the Database and Importing the AAC dataset (optional):

This AAC database is already included in this repository. If you delete it or need to re-create it, run the following script in the ```/src``` directory:

```python import_data.py```

## Running the AAC Dashboard Application:

Run the ```AAC_Dashboard.py``` script:

```python AAC_Dashboard.py```
