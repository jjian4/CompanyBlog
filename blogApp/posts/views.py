from flask import render_template,url_for, redirect,request,Blueprint
from flask_login import current_user,login_required
from blogApp import db
from blogApp.models import Post, Reply
from blogApp.posts.forms import NewPostForm, NewReplyForm

posts = Blueprint('posts',__name__)


#Create post
@posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = NewPostForm()

    if form.validate_on_submit():

        post = Post(title=form.title.data,
                    department=form.department.data,
                    text=form.text.data,
                    user_id=current_user.id
                    )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('core.department', department=form.department.data))

    return render_template('create_post.html',form=form, page_title='Create Post')


#View post (With option to reply to post)
@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    # Get the requested blog post by id number or return 404
    post = Post.query.get_or_404(post_id)
    # Get the replies to the post
    replies = Reply.query.filter_by(parent_post=post).order_by(Reply.date.desc())

    # Form for adding a new reply
    form = NewReplyForm()
    if form.validate_on_submit():

        new_reply = Reply(text=form.text.data,
                        post_id=post.id,
                        )
        db.session.add(new_reply)
        db.session.commit()
        return redirect(url_for('posts.view_post', post_id=post_id))

    return render_template('view_post.html', form=form, post=post, replies=replies)


#Update post
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    #Deny access if the author is not current_user
    if post.author != current_user:
        abort(403)

    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.department = form.department.data
        post.text = form.text.data
        db.session.commit()
        return redirect(url_for('core.department', department=post.department))

    #Get the post info to prefill the update form
    elif request.method == 'GET':
        form.title.data = post.title
        form.department.data = post.department
        form.text.data = post.text

    return render_template('create_post.html', form=form, page_title='Update Post')



#Delete post
@posts.route("/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    #Deny access if the author is not current_user
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('core.index'))








