from flask import render_template,request,Blueprint
from blogApp.models import Post

core = Blueprint('core',__name__)

#Website home Page
@core.route('/')
def index():
	#To display and paginate the posts
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=10)
	return render_template('index.html', posts=posts)


#About page
@core.route('/about')
def about():
    return render_template('about.html')
