# -*- coding: utf-8 -*-
#
from datetime import datetime, timedelta

import pytz
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from .base import LogStorage


class ESStorage(LogStorage):

    def __init__(self, config):
        hosts = config.get("HOSTS")
        kwargs = config.get("OTHER", {})
        self.index = config.get("INDEX") or 'jumpserver'
        self.doc_type = config.get("DOC_TYPE") or 'command_store'
        ignore_verify_certs = kwargs.pop('IGNORE_VERIFY_CERTS', False)
        if ignore_verify_certs:
            kwargs['verify_certs'] = None
        self.es = Elasticsearch(hosts=hosts, **kwargs)

    @staticmethod
    def make_data(command):
        data = dict(
            user=command["user"], asset=command["asset"],
            system_user=command["system_user"], input=command["input"],
            output=command["output"], risk_level=command["risk_level"],
            session=command["session"], timestamp=command["timestamp"],
            org_id=command["org_id"]
        )
        data["date"] = datetime.fromtimestamp(command['timestamp'], tz=pytz.UTC)
        return data

    def bulk_save(self, command_set, raise_on_error=True):
        actions = []
        for command in command_set:
            data = dict(
                _index=self.index,
                _type=self.doc_type,
                _source=self.make_data(command),
            )
            actions.append(data)
        return bulk(self.es, actions, index=self.index, raise_on_error=raise_on_error)

    def save(self, command):
        """
        保存命令到数据库
        """
        data = self.make_data(command)
        return self.es.index(index=self.index, doc_type=self.doc_type, body=data)

    @staticmethod
    def get_query_body(match=None, exact=None, date_from=None, date_to=None):
        if date_to is None:
            date_to = datetime.now()
        if date_from is None:
            date_from = date_to - timedelta(days=7)

        time_from = date_from.timestamp()
        time_to = date_to.timestamp()

        body = {
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [],
                    "filter": [
                        {"range": {
                            "timestamp": {
                                "gte": time_from,
                                "lte": time_to,
                            }
                        }}
                    ]
                }
            },
            "sort": {
                "timestamp": {
                    "order": "desc",
                }
            }
        }
        if match:
            for k, v in match.items():
                # 默认组织的org_id为""
                if k == 'org_id' and v == '':
                    body["query"]["bool"]["must_not"].append({"wildcard": {k: "*"}})
                    continue
                body["query"]["bool"]["must"].append({"match": {k: v}})
        if exact:
            for k, v in exact.items():
                body["query"]["bool"]["filter"].append({"term": {k: v}})
        return body

    def filter(self, date_from=None, date_to=None,
               user=None, asset=None, system_user=None,
               input=None, session=None, risk_level=None, org_id=None):

        match = {}
        exact = {}

        if user:
            exact["user"] = user
        if asset:
            exact["asset"] = asset
        if system_user:
            exact["system_user"] = system_user

        if session:
            match["session"] = session
        if input:
            match["input"] = input
        if org_id is not None:
            match["org_id"] = org_id
        if risk_level is not None:
            match['risk_level'] = risk_level

        body = self.get_query_body(match, exact, date_from, date_to)

        # Get total count (Because default size=10)
        data = self.es.search(index=self.index, doc_type=self.doc_type, body=body, size=0)
        total = data["hits"]["total"]
        if isinstance(total, dict) and isinstance(total.get('value'), int):
            total = total['value']

        if not isinstance(total, int):
            error = 'Request size type is not int: {} got'.format(type(total))
            raise ValueError(error)
        data = self.es.search(index=self.index, doc_type=self.doc_type, body=body, size=total)
        return data["hits"]

    def count(self, date_from=None, date_to=None,
              user=None, asset=None, system_user=None,
              input=None, session=None):
        match = {}
        exact = {}

        if user:
            exact["user"] = user
        if asset:
            exact["asset"] = asset
        if system_user:
            exact["system_user"] = system_user

        if session:
            match["session"] = session
        if input:
            match["input"] = input
        body = self.get_query_body(match, exact, date_from, date_to)
        del body["sort"]
        data = self.es.count(index=self.index, doc_type=self.doc_type, body=body)
        return data["count"]

    def __getattr__(self, item):
        return getattr(self.es, item)

    def all(self):
        """返回所有数据"""
        raise NotImplementedError("Not support")

    def ping(self):
        try:
            return self.es.ping()
        except Exception:
            return False
