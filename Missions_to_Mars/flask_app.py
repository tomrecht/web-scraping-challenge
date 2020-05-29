#!/usr/bin/python3

from flask import Flask, redirect, render_template
from jinja2 import Markup
from mission_to_mars import scrape
import pymongo
import json

app = Flask(__name__)

@app.route('/scrape')
def scrapenow():
    mars = scrape()
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.marsdata
    db['data'].drop()
    data = db['data']
    data.insert_one(mars)
    
    return redirect('..')

@app.route('/')
def home():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.marsdata
    data = db['data'].find_one()
    news_title = data['news_title']
    featured_image_url = data['featured_image_url']
    facts_table = data['facts_html']
    img1_url = data['images'][0]['img_url']
    img2_url = data['images'][1]['img_url']
    img3_url = data['images'][2]['img_url']
    img4_url = data['images'][3]['img_url']
    
    
    return(render_template("index.html", news_title = news_title, featured_image_url = featured_image_url, facts_table = Markup(facts_table), img1_url = img1_url, img2_url = img2_url, img3_url = img3_url, img4_url = img4_url))
        
        
if __name__ == "__main__":
    app.run(debug=True)
