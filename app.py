from flask import Flask, request, render_template, redirect
import random
import string
import json

app=Flask(__name__)
json_file="urls.json"

def read_urls():
    try:
        with open(json_file,"r") as file:
            #returning file in dictionary format
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_urls(data):
    with open(json_file,"w") as file:
        json.dump(data,file,indent=4)

def shortening_url():
    #generating all uppercase and lowercase letters along with numbers
    chars=string.ascii_letters+string.digits
    short_url_path="".join(random.choice(chars) for _ in range(6))
    return short_url_path

@app.route("/",methods=["POST","GET"])
def index():
    if request.method=="POST":
        #Taking url from user
        long_url=request.form["user_url"]

        #storing data from json to a dictionary
        shortend_urls=read_urls()

        #checking whether the same long url was previously entered by the user
        for short_url, url in shortend_urls.items():
            if url==long_url:
                return f"Shortened URL: {request.url_root}{short_url}"
            
        #shortening the url
        short_url=shortening_url()

        #if generated short url is same as one already randomly generated string
        while short_url in shortend_urls:
            short_url=shortening_url()
        
        #storing in dictionary then json
        shortend_urls[short_url]=long_url
        write_urls(shortend_urls)

        return f"Shortend URL: {request.url_root}{short_url}"
    return render_template("index.html")

@app.route("/<short_url>")
def rendering(short_url):
    shortend_urls=read_urls()
    long_url=shortend_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "Wrong URL", 404

if __name__=="__main__":
    app.run(debug=True)