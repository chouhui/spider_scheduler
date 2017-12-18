# -*- coding: utf-8 -*-

import requests

from spider_scheduler.models.jobs import jobs


def open_spider(url, project, spider):
    response = requests.post(url + 'schedule.json', data={"project": project, "spider": spider})
    return


def cancel_spider(url, project, spider):
    js = jobs().all('running')
    if js:
        for j in js:
            if j["spider"] == spider:
                job_id = j["id"]
                return requests.post(url + 'cancel.json', data={"project": project, "job": job_id})
