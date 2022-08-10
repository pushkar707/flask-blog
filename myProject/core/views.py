from flask import render_template,Blueprint, request
from myProject.models import Post
from flask_login import current_user

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page,per_page=6)
    return render_template('home.html',posts=posts)

@core.route('/blog')
def blog():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page,per_page=5)
    return render_template('blog.html',posts=posts)