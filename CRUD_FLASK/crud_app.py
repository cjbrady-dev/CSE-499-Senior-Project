from flask import Flask, render_template, request
import pickle, time, os
from flask_apscheduler import APScheduler
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('dictionary_file.pkl'):
    dictionary = {}
    with open('dictionary_file.pkl', 'wb') as file:
        pickle.dump(dictionary, file)


execute_clear_dictionary = APScheduler()

# Homepage
@app.route("/")
def crud_page():
    return render_template("/choose_crud_command.html")

# POST
@app.route("/post_elements")
def post_page():
    return render_template("/post_elements.html")

# PUT
@app.route("/put_elements", methods=["GET", "POST"])
def add_put_elements():
    if request.method == "GET":
        return render_template("/put_elements.html")
    else:
        #Load dictionary
        with open('dictionary_file.pkl', 'rb') as file:
            dictionary = pickle.load(file)

        key = request.form["entry1"]

        if key in dictionary:
            #Get new form fields
            new_breed = request.form['breed']
            new_age = request.form['age']
            new_pedigree = request.form['pedigree']
            new_description = request.form['description']
            file = request.files.get('image')

            #Update image if a new one is uploaded
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                dictionary[key]['image'] = filename # Only update image if provided

            # Update other item fields
            dictionary[key]['breed'] = new_breed
            dictionary[key]['age'] = new_age
            dictionary[key]['pedigree'] = new_pedigree
            dictionary[key]['description'] = new_description

            # Save updated dictionary
            with open('dictionary_file.pkl', 'wb') as file:
                pickle.dump(dictionary, file)

            generate_animals_html(dictionary)
            
            return render_template("/success.html")
        else:
            return render_template("error.html")

# Update Dictionary
@app.route("/success", methods=['POST'])
def success():
    # Load dictionary from pickle
    with open('dictionary_file.pkl', 'rb') as file:
        dictionary = pickle.load(file)

    # Get form fields
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']
    pedigree = request.form['pedigree']
    description = request.form['description']

    #Handle image file(s)
    file = request.files.get('image')

    if file and file.filename != '':
    #Handle no file uploaded case
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None


    #Save all data including image filename
    dictionary[name] = {
        'image': filename,
        'name': name,
        'breed': breed,
        'age': age,
        'pedigree': pedigree,
        'description': description
    }

    # Save back to pickle file
    with open('dictionary_file.pkl', 'wb') as file:
        pickle.dump(dictionary, file)

    generate_animals_html(dictionary)

    return render_template("/success.html")

# GET
@app.route("/get_page")
def the_get_page():
    file = open('dictionary_file.pkl', 'rb')
    retrieve_dictionary = pickle.load(file)
    file.close()

    return render_template("/get_page.html", retrieve_dictionary=retrieve_dictionary)

# Delete
@app.route("/delete_page")
def the_delete_page():
    file = open('dictionary_file.pkl', 'rb')
    retrieve_dictionary = pickle.load(file)
    file.close()

    return render_template("/delete_page.html", retrieve_dictionary=retrieve_dictionary)

@app.route("/delete_element", methods=['POST'])
def delete_element():
    #Load dictionary
    with open('dictionary_file.pkl', 'rb') as file:
        dictionary = pickle.load(file)

    key = request.form["entry1"]

    if key in dictionary:
        del dictionary[key]

        #save updated dictionary
        with open("dictionary_file.pkl", 'wb') as file:
            pickle.dump(dictionary, file)

            generate_animals_html(dictionary)

        return render_template("/delete_success.html")
    else:
        return render_template("/error.html")
    
def clear_dictionary():
    try:
        if os.path.exists("dictionary_file.pkl"):
            os.remove("dictionary_file.pkl")
    except Exception as e:
        print(f"Error deleting pickle file: {e}")

    dictionary = {}
    with open("dictionary_file.pkl", 'wb') as file:
        pickle.dump(dictionary, file)


# Path to the Brady's Farm website folder
def generate_animals_html(dictionary):
    output_folder = os.path.join("..", "Brady's Farm")
    output_path = os.path.join(output_folder, "page2.html")

    # Make sure folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Convert dictionary to list if needed
    if isinstance(dictionary, dict):
        animals = list(dictionary.values())
    else:
        animals = dictionary

    # Start of HTML content
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brady's Farm Animals</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <main>
        <img id="mainLogo" src="images/Black Retro Animal Farm Logo.jpg">
    </main>
    <h1>Brady's Farm Animals</h1>
"""

    # Loop through each animal in the list
    for item in animals:
        html_content += f"""
    <div id="item-container">
        <div class="item">
            <img src="../CRUD_FLASK/static/uploads/{item['image']}" alt="{item['name']}"><br>
            <strong>Name:</strong> {item['name']}<br>
            <strong>Breed:</strong> {item['breed']}<br>
            <strong>Age:</strong> {item['age']}<br>
            <strong>Pedigree:</strong> {item['pedigree']}<br>
            <strong>Description:</strong> {item['description']}<br>
        </div>
    </div>


        <hr>
"""

    # Close HTML tags
    html_content += """
        <footer>
            <nav>
                <ul>
                    <li><b><a href="index.html">Home</a></b></li>
                    <li><b><a href="page2.html">page 2</a></b></li>
                </ul>
            </nav>
        </footer>
</body>
</html>
"""

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML written to {output_path}")
    

if __name__== '__main__':
    # execute_clear_dictionary.add_job(id = 'Scheduled Task', func=clear_dictionary, trigger="interval", seconds=300)
    execute_clear_dictionary.start()
    app.run(host="0.0.0.0", debug=True, port=5000)