from flask import Flask, render_template, request
from contact import Contact

app = Flask(__name__, template_folder='A')
app.config['SECRET_KEY'] = 'key'



db = []


## View Function ##############

@app.route('/',methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/saved', methods=["POST"])
def saved():

    username = request.form['client_name']
    input_name = request.form['Name']
    input_number = request.form['Number']           # Request the inputs

    userslist = [ i.client_name for i in db ]       # create a list of all users (phonebook owners)
    entry = (input_name,input_number)               # create a tuple of their entry 
    
    presence = username in set(userslist)           # check to see whether the user is new or old
    
    if presence:                    # for OLD USERS: 

        user_index = userslist.index(username)      # find it's index in the database (db list)
        db[user_index].saver(entry)                 # update the db instance with the given entry
        contactlist = db[user_index].reporter()     # Get a __repr__ of the Contact object
        
        
    else:                           # for NEW USERS:
        phonebook = Contact(username)               # Create a new Contact object
        phonebook.saver(entry)                      # save the entry into that object
        contactlist = phonebook.reporter()          # Get a __repr__ of the Contact object
        db.append(phonebook)                        # add the newly created Contact object to the db
        

    return render_template('index.html' , mylist=contactlist, username = username,  db = db)

if __name__ == '__main__':
    app.run(debug = True)
