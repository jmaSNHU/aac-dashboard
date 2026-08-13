![AAC Outcomes Dashboard](https://jmasnhu.github.io/images/aac-dashboard.jpg)

# Austin Animal Center Outcomes Dashboard
Enhancement for CS-340's AAC Outcomes Dashboard that replaces the original MongoDB database with SQLite and normalizes the Austin Animal Center's outcomes dataset. This project is built using Python and the SQLAlchemy ORM for data access on the backend. The frontend dashboard is implemented with the Plotly Dash framework.

This purpose of this app is to provide searching and filter for certain types of rescue animals. Currently, the app provide options for water, mountain and disaster rescue. Data visualization tools include a bar and histogram charts, as well as a geolocation chart that places a map pin for the currently selected animal's latitude and longitude coordinates.

## Getting Started

To run the code, you must first activate the Python virtual environment included in the repository:

```source myenv/bin/activate```

## Creating the Database and Importing the AAC dataset (optional):

This AAC database is already included in this repository. If you delete it or need to re-create it, run the following script in the ```/src``` directory:

```python import_data.py```

## Running the AAC Dashboard Application:

Run the ```AAC_Dashboard.py``` script:

```python AAC_Dashboard.py```
