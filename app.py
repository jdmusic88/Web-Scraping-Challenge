## Step 1 - Scraping
## Step 2 - MongoDB and Flask Application

# Import Dependencies 
from flask import Flask, redirect, render_template, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import time

# Create an instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Can try this
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app_app"
#mongo = PyMongo(app)



# Create route that renders index.html template then finds documents from mongo
@app.route("/")
def index(): 
 
    # Find data
    mars_info = mongo.db.collection.find_one()
    print(mars_info)
    print("did you get here")

    # Return template and data
    return render_template("index.html", mars_web=mars_data)


# Route that will trigger scrape function

@app.route("/scrape")
def scrape():

        # Run the scrape functions


        mars_info = mongo.db.collection
        print("did you get the data?")
        mars_data = scrape_mars.scrape_mars_data()

        print(mars_info)

        # Run the scrape_data
        mars_info.update({}, mars_data, upsert=True)
        return redirect("/")
        
    if __name__ == "__main__": 

            app.run(debug= True)