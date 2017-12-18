# -*- coding: utf-8 -*-
import commands
import threading

import requests
from flask import (
    Blueprint,
    redirect,
    url_for,
    render_template
)
from models import save
from models.distributed_crawl import distributed_crawl
from models.projects import project

from spider_scheduler.models.jobs import jobs
from spider_scheduler.threading_op import cancel_spider as cancel
from spider_scheduler.threading_op import open_spider as open

main = Blueprint('scrapyd', __name__)


#项目列表(主页)
@main.route('/project_list', methods=['GET'])
def project_list():
    response = requests.get('http://localhost:6800/listprojects.json')
    subject = project()
    path = subject.db_path()
    save(response.json(), path)
    return redirect(url_for('index.index'))


#删除项目
@main.route('/del_project/<project>', methods=['GET'])
def del_project(project):
    response = requests.post('http://127.0.0.1:6800/delproject.json', data={"project": project})
    print response.content
    return redirect(url_for('scrapyd.project_list'))


#爬虫运行状态
@main.route('/state', methods=['GET'])
def spider_state():
    response = requests.get('http://localhost:6800/listjobs.json?project=distributed_crawl')
    state = jobs()
    path = state.db_path()
    save(response.json(), path)
    pending = state.all('pending')
    running = state.all('running')
    finish = state.all('finished')
    return render_template('state.html', pending=pending, running=running, finish=finish)


#爬虫列表
@main.route('/spider_list/<project>', methods=['GET'])
def crawl_jobs(project):
    response = requests.get('http://localhost:6800/listspiders.json?project=' + project)
    subject = distributed_crawl()
    path = subject.db_path()
    save(response.json(), path)
    spiders = subject.all('spiders')
    return render_template('list.html',spiders=spiders)


#开启爬虫
@main.route('/open/<spider>', methods=['GET'])
def open_spider(spider):
    t1 = threading.Thread(target=open, name='Thread_1', args=('http://localhost:6800/', 'distributed_crawl', spider,))
    t2 = threading.Thread(target=open, name='Thread_2', args=('http://localhost:6800/', 'distributed_crawl', spider,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return redirect(url_for('scrapyd.spider_state'))

#关闭爬虫
@main.route('/cancel/<spider>', methods=['GET'])
def cancel_spider(spider):
    t1 = threading.Thread(target=cancel, name='Thread_1', args=('http://localhost:6800/', 'distributed_crawl', spider,))
    t2 = threading.Thread(target=cancel, name='Thread_2', args=('http://localhost:6800/', 'distributed_crawl', spider,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return redirect(url_for('scrapyd.spider_state'))


#更新代码
@main.route('/manager/<project>')
def manager_project(project):
    cmd = "cd %s;git clone %s" % "/Users/qmp/PycharmProjects/spider_scheduler", "git@github.com:chouhui/spider_scheduler.git"
    commands.getstatusoutput(cmd)


#部署代码
@main.route('/deploy/<project>')
def deploy_project(project):
    cmd = "cd %s;%s" % ("/Users/qmp/PycharmProjects",
                        "scrapyd-deploy dis -p distributed_crawl --version ver2017.")
    commands.getstatusoutput(cmd)