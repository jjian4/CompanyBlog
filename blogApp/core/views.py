from flask import render_template,request,Blueprint
#To display posts and replies in index.html and department.html
from blogApp.models import Post, Reply


core = Blueprint('core',__name__)


#Website home Page
@core.route('/')
def index():
	#To display and paginate the posts
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=6)
	replies = Reply.query.order_by(Reply.date.desc())
	return render_template('index.html', posts=posts, replies=replies)


@core.route('/department/<department>')
def department(department):
	#To display and paginate the posts
	page = request.args.get('page', 1, type=int)

	department_posts = Post.query.filter_by(department=department).order_by(Post.date.desc()).paginate(page=page, per_page=3)

	replies = Reply.query.order_by(Reply.date.desc())

	title = department
	return render_template('department.html', title=title, department_posts=department_posts, replies=replies)


#About page
@core.route('/about')
def about():
    return render_template('about.html')
