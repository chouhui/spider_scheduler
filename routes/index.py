
from flask import (
    render_template,
    Blueprint,
)

from spider_scheduler.models import project

main = Blueprint('index', __name__)


@main.route('/', methods=['GET'])
def index():
    p = project()
    projects = p.all('projects')
    return render_template('index_1.html',projects=projects)