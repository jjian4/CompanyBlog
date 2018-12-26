from flask import render_template,request,Blueprint

core = Blueprint('core',__name__)

#Website home Page
@core.route('/')
def index():
    return render_template('index.html')


#About page
@core.route('/about')
def about():
    return render_template('about.html')
