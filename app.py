from flask import Flask
import requests
import json
import sqlite3


app = Flask(__name__)


VALID_STATES = {"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"}

def get_bird(state: str):
    if state not in VALID_STATES:
        return json.dumps({"error": "Invalid state abbreviation"})

    try:
        conn = sqlite3.connect("./birds.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM birds WHERE abbreviation = ?"
        cursor.execute(query, (state,))
        rows = cursor.fetchall()
        list_accumulator = []
        for item in rows:
            print(item)
            list_accumulator.append({k: item[k] for k in item.keys()})

        return json.dumps(list_accumulator)
    except sqlite3.Error as e:
        return json.dumps({"error": "Database error"})
    finally:
        if conn:
            conn.close()


def get_weather(state: str):
    r = requests.get(f'https://api.weather.gov/alerts/active?area={state}')
    return r.json()


@app.get('/')
def hello():
    return "Add a 2 letter state param to learn about birds and the weather challenges they face.", \
           200, \
           {'Content-Type': 'text/html; charset=utf-8'}


@app.get('/<state>')
def bird(state):

    bird = get_bird(state)
    print(bird)
    weather = get_weather(state)
    out = str([bird, weather])
   
    return out, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

