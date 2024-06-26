from flask import Flask, redirect, render_template, url_for, request, send_file
import os
import geocoder
import requests
from dotenv import load_dotenv
from io import BytesIO

app = Flask(__name__)
api_key = os.getenv('api')


def configure():
  load_dotenv()

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search", methods=['POST', 'GET'])
def get_places_data():
  if request.method == 'POST':
    location = request.form['location']
    category = request.form['category']
    limit = request.form['limit']

    print(location)
    try:
      g = geocoder.osm(location)  # Using OpenStreetMap geocoder
      if not g.ok:
        raise ValueError(f"Geocoding failed for {location}. Status: {g.status}")

      lat, lon = g.latlng
    except Exception as error:
      return render_template("error.html", error_message=str(error))
    
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
      return render_template("places.html", d=data['results'])
    else:
      return f"Error: {response.status_code}", response.status_code
  
  return render_template("search.html")

@app.route("/details/<fsq_id>")
def get_places_details(fsq_id):
  headers = {
    "accept": "application/json",
    "Authorization": api_key
  }
  url1 = f"https://api.foursquare.com/v3/places/{fsq_id}"
  
  resp1 = requests.get(url=url1, headers=headers)
  data1 = resp1.json()
  place_name = data1['name']
  # Fetch photos from the Foursquare API
  resp = requests.get(url=f"https://api.foursquare.com/v3/places/{fsq_id}/photos", headers=headers)
  data = resp.json()
  print(data)
  return render_template("details.html", d=data, place_name=place_name)

@app.route('/fetch-image')
def fetch_image():
  prefix = request.args.get('prefix', '')
  suffix = request.args.get('suffix', '')
  img_url = "".join([prefix, "original", suffix])
  
  response = requests.get(img_url)
  if response.status_code == 200:
      img = BytesIO(response.content)
      return send_file(img, mimetype='image/jpeg')
  else:
      return "Image not found", 404
    

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/contact")
def contact():
  return render_template("contact.html")

if __name__ == "__main__":
  configure()
  app.run(debug=True)
