# -*- coding:utf-8 -*-

import requests
import threading


class Crawl_method(object):

    def __init__(self, url):
        # threading.Thread.__init__(self,name=name)
        self.url = url

    def state(self):
        return requests.get(self.url+'daemonstatus.json')

    def project_list(self):
        return requests.get(self.url+'listprojects.json')

    def crawl_list(self, project):
        response = requests.get(self.url+'listprojects.json?project='+project)
        return response.content

    def crawl_jobs(self, project):
        response = requests.get(self.url+'listjobs.json?project='+project)
        return response.content

    def open_spider(self, project, spider):
        response = requests.post(self.url+'schedule.json', data={"project": project, "spider": spider})
        return response.content

    def del_version(self, project, version):
        return requests.post(self.url+'delversion.json', data={"project": project, "version": version})

    def del_project(self, project):
        return requests.post(self.url+'delproject.json', data={"project": project})

    def add_version(self, project, version):
        return requests.post(self.url+'addversion.json', data={"project": project, "version": version})

    def cancel(self, project, jobid):
        return requests.post(self.url+'cancel.json', data={"project": project, "job": jobid})