from flask import Flask, render_template, request, flash, redirect, url_for,send_file
import os
from canvasapi import Canvas
from werkzeug.utils import secure_filename

API_URL = "https://canvas.oregonstate.edu/"
# Canvas API key
API_KEY = "1002~m1ShsxLu5bZY6SbSd5KlXjN9ejluixXwRFVYDvVQhGjIMx46dLJqS81NfZtCeTRJ"

app = Flask(__name__,template_folder='templates')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def log_request():
    app.logger.debug("Request Headers %s", request.headers)
    return None
@app.route('/clientID/<clientID>',methods=["GET","POST"])
def getHomework(clientID=None):
    canvas = Canvas(API_URL, clientID)
    course = canvas.get_course(1799013)
    assigments=course.get_assignments()
    assNameList=[item.name for item in assigments]
    assIDList=[item.id for item in assigments]
    # return str(clientID)
    return render_template("assList.html",len=len(assNameList),Ass=assNameList,AssID=assIDList,title=course.name)
@app.route('/clientID/<clientID>/course/<courseID>',methods=["GET","POST"])
def getHomeworkwiCourse(clientID=None,courseID=None):
    canvas = Canvas(API_URL, clientID)
    course = canvas.get_course(courseID)
    assigments=course.get_assignments()
    assNameList=[item.name for item in assigments]
    assIDList=[item.id for item in assigments]
    # return str(clientID)
    return render_template("assList.html",len=len(assNameList),Ass=assNameList,AssID=assIDList,title=course.name)

@app.route('/submit', methods=['POST'])
def upload_file():
    print('received!!')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/download/<fileName>",methods=["POST","GET"])
def downloadFile(fileName):
    path = fileName
    return send_file(path, as_attachment=True)
@app.route("/try",methods=["POST","GET"])
def test():
    print(request.form)
    return str("request.form")



if __name__ == "__main__":  
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['JSON_AS_ASCII'] = False
    app.config['UPLOAD_FOLDER']="static/uploadStack"
    app.run(host='0.0.0.0', port='2333',ssl_context='adhoc')