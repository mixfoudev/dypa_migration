from flask import Flask, request, render_template, redirect, url_for, flash
import os
import pymysql
from werkzeug.utils import secure_filename
from flask import session
from validation import validate

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit
 # Database connection
app.config['DB'] = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    cursorclass=pymysql.cursors.DictCursor
)



ALLOWED_EXTENSIONS = {'xlsx'}


REQUIRED_COLUMNS = [
    "ΤΜΗΜΑ", "ΑΚΑΔ. ΕΤΟΣ", "ΕΙΔΙΚΟΤΗΤΑ", "ΤΑΞΗ", "ΑΦΜ", "ΕΠΩΝΥΜΟ", "ΟΝΟΜΑ",
    "ΕΠΩΝΥΜΟ ΠΑΤΕΡΑ", "ΟΝΟΜΑ ΠΑΤΕΡΑ", "ΕΠΩΝΥΜΟ ΜΗΤΕΡΑΣ", "ΟΝΟΜΑ ΜΗΤΕΡΑΣ",
    "ΗΜ/ΝΙΑ ΓΕΝΝΗΣΗΣ", "ΦΥΛΟ", "EMAIL", "ΚΙΝΗΤΟ ΤΗΛ", "ΣΤΑΘΕΡΟ ΤΗΛ",
    "ΔΙΕΥΘΥΝΣΗ", "ΑΡΙΘΜΟΣ", "ΠΟΛΗ", "ΤΚ", "ΑΜΚΑ", "ΑΜΑ", "ΤΟΠΟΣ ΓΕΝΝΗΣΗΣ",
    "ΔΗΜΟΣ ΕΓΓΡΑΦΗΣ", "ΑΡ. ΔΗΜΟΤΟΛΟΓ", "ΧΩΡΑ", "IBAN", "ΑΜ ΑΡΡΕΝΩΝ",
    "ΤΟΠ ΕΓΓ Μ.Α", "ΚΠΑ", "ΠΑΡΑΚΟΛΟΥΘΕΙ ΜΑΘΗΜΑΤΑ ΓΕΝ ΠΑΙΔΕΙΑΣ", "ΑΜ",
    "ΗΜΝΙΑ ΕΓΓΡΑΦΗΣ", "ΑΚΑΔ. ΕΤΟΣ ΕΓΓΡΑΦΗΣ", "ΣΧΟΛΗ"
]

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        school = request.form.get("school")
        print(school)
        if file.filename == "":
            flash("Δεν επιλέχθηκε αρχείο")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            #data = validate.validate_school(school, filepath)
            try:
                #error_rows, section_students, students = validate.validate_school(school, filepath)
                data = validate.validate_school(school, filepath)
                print("erors: ",len(data['errors']))
            except Exception as e:
                print(f"Αδυναμία ανάγνωσης αρχείου: {e}")
                flash(f"Αδυναμία ανάγνωσης αρχείου")
                return redirect(request.url)
            finally: os.remove(filepath)

            session['data'] = data
            return redirect(url_for("upload_file"))

        else:
            flash("Μη έγκυρο αρχείο.")
            return redirect(request.url)
    ##
    data = session.pop('data', None)
    print(data)
    #data = []
    return render_template("upload.html", data=data)



""" @app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        school = request.form.get("school")
        print(school)
        if file.filename == "":
            flash("Δεν επιλέχθηκε αρχείο")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            
            # missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
            # if missing_columns:
            #     return render_template("upload.html", missing_columns=missing_columns)
            
            try:
                error_rows = validate.validate_school(school, filepath)
                print("erors: ",len(error_rows))
            except Exception as e:
                flash(f"Αδυναμία ανάγνωσης αρχείου: {e}")
                return redirect(request.url)
            #finally: os.remove(filepath)


            return render_template("upload.html", errors=error_rows, success=len(error_rows) ==0)

        else:
            flash("Μη έγκυρο αρχείο.")
            return redirect(request.url)

    return render_template("upload.html", errors=None) """

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)