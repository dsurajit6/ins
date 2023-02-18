from flask import Flask, render_template, send_file
from bson.objectid import ObjectId
from scrapper import Scrapper
from mongo_operation import MongoOperation
from base_urls import S3_BUCKET

application = Flask(__name__)
app = application

@app.route("/")
def home():
    mo = MongoOperation()
    moc = mo.get_collection()
    data = moc.find({})
    return render_template("index.html", data=data)

@app.route('/details/<cid>')
def course_details(cid):
    mo = MongoOperation()
    moc = mo.get_collection()
    course_data = moc.find_one({"_id": ObjectId(cid)})
    return render_template("course_details.html", course_details=course_data)


@app.route("/refresh")
def refresh():
    scrapper = Scrapper()
    file_names = scrapper.course_operations()
    if len(file_names) > 0:
       msg = "Success"
    else:
        msg = "Error"
    return render_template("refresh.html", msg = msg)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)

