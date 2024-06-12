from flask import Flask, redirect, render_template, url_for, request
import os
import geocoder
import requests

app = Flask(__name__)

api_key = "fsq3MbEqqgZHgwaIewUEDEN/fGb2WACJfp/X6aEyVfKG4ww="

@app.route("/search", methods=['POST', 'GET'])
def get_places_data():
  if request.method == 'POST':
    location = request.form['location']
    category = request.form['category']
    limit = request.form['limit']

    g = geocoder.osm(location)  # Using OpenStreetMap geocoder
    if g.ok:
        lat, lon = g.latlng
    else:
        return "Location not found", 400
    
    ll = f"{lat},{lon}"
    
    params = {
        "ll": ll,
        "query": category,
        "sort": "RELEVANCE",
        "limit": limit
    }
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
      data = response.json()
      # return render_template("results.html", data=data)
      print(data)
      return redirect(url_for("places"))
    else:
      return f"Error: {response.status_code}", response.status_code
  
  return render_template("search.html")


@app.route("/places")
def places():
  return render_template("places.html")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
