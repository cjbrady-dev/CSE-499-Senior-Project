from flask import Flask, render_template, request
import pickle, time, os
from flask_apscheduler import APScheduler
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

global dictionary
dictionary = {}
file = open("dictionary_file.pkl", 'wb')
pickle.dump(dictionary, file)
file.close()


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
@app.route("/put_elements")
def add_put_elements():
    dictionary = {}
    file = open("dictionary_file.pkl", 'wb')
    pickle.dump(dictionary, file)
    file.close()
    return render_template("/put_elements.html")

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
    file = open('dictionary_file.pkl', 'rb')
    dictionary = pickle.load(file)
    file.close()
    key = request.form["entry1"]

    if key in dictionary.key():
        del dictionary[key]
        file = open("dictionary_file.pkl", 'wb')
        pickle.dump(dictionary, file)
        file.close()
        time.sleep(1)
        return render_template("/delete_success.html")
    else:
        return render_template("/error.html")
    
def clear_dictionary():
    os.remove("dictionary_file.pkl")
    dictionary = {}
    file = open("dictionary_file.pkl", 'wb')
    pickle.dump(dictionary, file)
    file.close()

# Path to the Brady's Farm website folder
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
    <title>Brady's Farm Animals</title>
    <style>
        body { background-color: black; color: white; font-family: Arial, sans-serif; }
        .animal { border: 1px solid white; padding: 10px; margin: 10px; }
        img { max-width: 200px; height: auto; }
    </style>
</head>
<body>
    <h1>Brady's Farm Animals</h1>
"""

    # Loop through each animal in the list
    for item in animals:
        html_content += f"""
    <div class="animal">
        <img src="{item['image']}" alt="{item['name']}"><br>
        <strong>Name:</strong> {item['name']}<br>
        <strong>Breed:</strong> {item['breed']}<br>
        <strong>Age:</strong> {item['age']}<br>
        <strong>Pedigree:</strong> {item['pedigree']}<br>
        <strong>Description:</strong> {item['description']}<br>
    </div>
    <hr>
"""

    # Close HTML tags
    html_content += """
</body>
</html>
"""

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML written to {output_path}")
    

if __name__== '__main__':
    execute_clear_dictionary.add_job(id = 'Scheduled Task', func=clear_dictionary, trigger="interval", seconds=300)
    execute_clear_dictionary.start()
    app.run(host="0.0.0.0", debug=True, port=5000)