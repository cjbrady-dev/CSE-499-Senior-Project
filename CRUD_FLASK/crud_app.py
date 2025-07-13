from flask import Flask, render_template, request, send_from_directory
import pickle, time, os
from flask_apscheduler import APScheduler
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRADYS_FARM_DIR = os.path.join(BASE_DIR, '..', 'Brady\'s Farm')


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

#files accessible via URLs
@app.route('/brady_static/<path:filename>')
def brady_static(filename):
    return send_from_directory(BRADYS_FARM_DIR, filename)

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
            
            files = request.files.getlist('image')
       
            if files and any(f.filename for f in files):
                dictionary[key].setdefault('images', [])
                for file in files:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    dictionary[key]['images'].append(filename)
            
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
    image_files = request.files.getlist('image')
    image_filenames = []

    for file in image_files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filenames.append(filename)
    
    #Handle video(s)
    video_files = request.files.getlist('video')
    video_filenames = []

    for file in video_files:
        if file and file.filename != '':
            ext = os.path.splitext(file.filename)[1].lower()
            if ext in {'.mp4', '.webm', '.ogg'}:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                video_filenames.append(filename)
            else:
                pass


    #Save all data including image filename
    dictionary[name] = {
        'images': image_filenames,
        'videos': video_filenames,
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
        if 'images' in dictionary[key]:
            for img_filename in dictionary[key]['images']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
        if 'videos' in dictionary[key]:
            for vid_filename in dictionary[key]['videos']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'] , vid_filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        del dictionary[key]

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



#  HTML generator – shows *all* images & videos
def generate_animals_html(dictionary):
    from flask import current_app 

    output_folder = BRADYS_FARM_DIR 
    output_path = os.path.join(output_folder, "page2.html")
    os.makedirs(output_folder, exist_ok=True)

    animals = list(dictionary.values()) if isinstance(dictionary, dict) else dictionary

    with current_app.app_context(): 
        rendered_html = render_template("animal_template.html", animals=animals)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)    


@app.route('/animals') 
def show_animals():
   
    try:
        with open('dictionary_file.pkl', 'rb') as file:
            dictionary = pickle.load(file)
    except FileNotFoundError:
        dictionary = {} 

    animals_data = list(dictionary.values())

   
    return render_template("animal_template.html", animals=animals_data)

if __name__== '__main__':
    execute_clear_dictionary.start()
    app.run(host="0.0.0.0", debug=True, port=5000)