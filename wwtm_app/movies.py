from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from modules import convert_results_to_dict, get_query_results

app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField("I'm looking for the movie where", validators=[DataRequired(), Length(10, 500)])
    submit = SubmitField('Submit')


# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        query = form.name.data
        # empty the form field
        form.name.data = ""
        return redirect( url_for('search_results', query=query) )
    return render_template('index.html', form=form)

@app.route('/search_results/<query>')
def search_results(query):
    results = get_query_results(query)
    if len(results) == 0:
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        results_dict = convert_results_to_dict(results)
        # pass all the data for the selected actor to the template
        return render_template('movies.html', query=query, results=results_dict)

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
