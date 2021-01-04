from flask import Flask, render_template, request
from contact import Contact, db

app = Flask(__name__, template_folder='A')
app.config['SECRET_KEY'] = 'key'

## View Function ##############

@app.route('/',methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/saved', methods=["POST"])
def saved():

    username = request.form['client_name']
    input_name = request.form['Name']
    input_number = request.form['Number']

    db.append( Contact(username , input_name , input_number) )
    
    contact_list = [i.entries['name'] for i in db]
    number_list = [i.entries['phone'] for i in db]
    owners_list = [i.entries['client_name'] for i in db]
    contactlist = list(zip(owners_list , number_list , contact_list))

    def entry_count(owners_list = owners_list):
        # This gonna be NASTY, Sorry!
        Z = owners_list # only to use shorter name!
        owner_freq = list(zip([Z.count(i) for i in set(Z)],set(Z)))
        
        reporter = []
        for i in owner_freq:
            reporter.append(f'{i[1]} has saved {i[0]} contact(s)')
        return reporter
        

    return render_template('index.html' , mylist=contactlist, username = username  , db = entry_count() )

if __name__ == '__main__':
    app.run(debug = True)
