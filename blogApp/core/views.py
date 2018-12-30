from flask import render_template, request, redirect, url_for, Blueprint
#To display posts and replies in index.html and department.html
from blogApp.models import Post, Reply
#For donation option on the About page
import stripe


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



#Stripe keys
public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

#About page
@core.route('/about')
def about():
    return render_template('about.html', public_key=public_key)

#Donation in the About page using Stripe
@core.route('/payment', methods=['POST'])
def payment():
	# Amount in cents
	amount = 2500

	customer = stripe.Customer.create(
	    email='customer@example.com',
	    source=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
	    customer=customer.id,
	    amount=amount,
	    currency='usd',
	    description='Flask Charge'
	)

	return redirect(url_for('core.confirm_payment'))




@core.route('/confirm_payment')
def confirm_payment():
	return render_template('confirm_payment.html')













