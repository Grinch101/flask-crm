from flask import Flask, render_template, request, flash, redirect, url_for
from contact import Contact

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

## View Function ##############

phonbook = Contact()
@app.route('/', methods=['GET','POST'])
def index():

    if request.form:
        
        input_name = request.form['Name']
        input_number = request.form['Number']
        username = request.form['client_name']
        phonbook.insert(username,input_name,input_number)

        flash(f'{input_number} for {input_name} has been saved')

        return redirect(url_for('index'))

    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)