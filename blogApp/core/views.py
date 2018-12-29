from flask import render_template,request,Blueprint
from blogApp.models import Post
from blogApp.posts.forms import NewPostForm

core = Blueprint('core',__name__)

#Navbar channel options - include departments names from NewPostForm
@core.context_processor
def inject_test():
	departments = NewPostForm.departments
	return dict(departments=departments)

#Website home Page
@core.route('/')
def index():
	#To display and paginate the posts
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=10)
	departments = NewPostForm.departments
	return render_template('index.html', posts=posts, departments=departments)


@core.route('/department/<department>')
def department(department):
	#To display and paginate the posts
	page = request.args.get('page', 1, type=int)

	department_posts = Post.query.filter_by(department=department).order_by(Post.date.desc()).paginate(page=page, per_page=10)

	posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=10)
	title = department
	return render_template('department.html', department_posts=department_posts, title=title)


#About page
@core.route('/about')
def about():
    return render_template('about.html')
