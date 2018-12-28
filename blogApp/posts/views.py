from flask import render_template,url_for, redirect,request,Blueprint, flash
from flask_login import current_user,login_required
from blogApp import db
from blogApp.models import Post
from blogApp.posts.forms import NewPostForm

posts = Blueprint('posts',__name__)


#Create post
@posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = NewPostForm()

    if form.validate_on_submit():

        post = Post(title=form.title.data,
                    text=form.text.data,
                    user_id=current_user.id
                    )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


#View post
@posts.route('/post/<int:post_id>')
def view_post(post_id):
    # grab the requested blog post by id number or return 404
    post = Post.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)


#Update post
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = BlogPost.query.get_or_404(post_id)
    #Deny access if the author is not current_user
    if post.author != current_user:
        abort(403)

    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('posts.update', post_id=post.id))

    #Get the post info to prefill the update form
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', form=form, title='Update')



#Delete post
@posts.route("/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    #Deny access if the author is not current_user
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('core.index'))



