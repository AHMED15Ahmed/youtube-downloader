import logging
from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from io import BytesIO
import secrets
from extractor import extract_video_data_from_url
from pytube import extract #Get youtube id
app = Flask(__name__)
app.config['SECRET_KEY'] = "335c13a551af4d60992e12f692a40de911e0315cd58a20041fa04cb540b4ff18"
#print(secrets.token_hex())#2d820bb0bcae7aacb104308c14593112074fb65e464b055066ce00fea287e221
@app.route("/home", methods = ["POST","GET"])
@app.route("/", methods = ["POST","GET"])
def home():
    if request.method=="POST":
        session["link"]=request.form.get('url')
        #print(session['link'])
        vd=extract_video_data_from_url(session["link"])
        # print(vd)
        try:
            url=YouTube(session["link"])
            # vd=extract_video_data_from_url(url)
            # print(vd)
            url.check_availability()
        except:
            return render_template("Error.html")
        return render_template("download.html",url=url,vd=vd)
        
    return render_template('home.html')
@app.route("/Error", methods = ["GET", "POST"])
def Error():
 return render_template("Error.html")
@app.route("/login", methods = ["GET", "POST"])
def login():
 return render_template("login.html")

@app.route("/download", methods = ["GET", "POST"])
def download():
    if request.method == "POST":
        buffer = BytesIO()
        try:
            url = YouTube(session['link'])
            itag = request.form.get("itag")
            video = url.streams.get_by_itag(itag)
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name="Video.mp4", mimetype="video/mp4")
            #Then use Flask's send_file() to download the video to the current Downloads folder. 
        except:
            logging.exception("Failed download")
            return "Video download failed!"
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)