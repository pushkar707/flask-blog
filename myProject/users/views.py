from flask import redirect,url_for,render_template,request,Blueprint
from myProject.models import User,Post
from myProject.users.forms import LoginForm,RegisterationForm, UpdateUserForm
from myProject import db
from flask_login import login_user, logout_user, login_required, current_user

from myProject.users.picture_handler import add_profile_pic

user = Blueprint('user',__name__)

@user.route('/register',methods=['GET','POST'])
def register():

    form = RegisterationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('register.html',form=form)

@user.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))
            
# Update User

@user.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        return redirect(url_for('user.account'))

    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)

@user.route('/<username>')
def blog_post(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = Post.query.filter_by(user=user).order_by(Post.date.desc()).paginate(page=page,per_page=5)
    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user,profile_image=profile_image)