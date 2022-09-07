from flask import Flask, render_template, redirect, url_for, request, send_file
from pdf import pdf_printer, downloadAll
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, validators
from datetime import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "adsfasdfxcşizxicv"
app.config["UPLOAD_FOLDER"] = "static"

X=0

class FileForm(FlaskForm):
    file = FileField("File",validators=[validators.InputRequired()])
    submit = SubmitField("Upload PDF")

@app.route("/")
def index():
    return "<a href='./pdfprinter'>PDFprinter</a>"

@app.route("/pdfprinter",methods=["GET","POST"])
def pdfprinter():
    form = FileForm()
    if request.method == "POST":
        global X
        pdf_printer(form.file.data,X)
        X+=1
        path = f"./static/{str(X-1)}/0.zip"
        return send_file(path, as_attachment=True)
    else:
        return render_template("pdfprinter.html",form=form)

@app.route("/pdfdownloader", methods=["GET","POST"])
def pdfdownloader():
    if request.method == "POST":
        url = request.form.get("pdfdownloader")
        downloadAll(url)
        path = f"./static/downloadAll/0.zip"
        return send_file(path, as_attachment=True)
    else:
        return render_template("pdfdownloader.html")

if __name__ == "__main__":
    app.run(debug=True, host="localhost")