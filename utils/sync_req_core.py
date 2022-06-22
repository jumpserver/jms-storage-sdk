#!/usr/bin/python
#
import os
import re

spliter = re.compile('[>=<]+')

core_req_path = os.environ.get("CORE_REQ_FILE")
if not core_req_path:
    raise ValueError("No CORE_REQ_FILE env found")

with open(core_req_path) as f:
    core_reqs = f.readlines()

core_reqs_mapper = {}
for req in core_reqs:
    pkg_version = spliter.split(req.strip())
    core_reqs_mapper[pkg_version[0]] = req.strip()

fixed_reqs = []
with open('../requirements.txt') as f:
    reqs = f.readlines()

for req in reqs:
    pkg_version = spliter.split(req)
    pkg = pkg_version[0]

    if pkg in core_reqs_mapper:
        req = core_reqs_mapper[pkg]
    fixed_reqs.append(req.strip() + '\n')


with open('../requirements.txt', 'w') as f:
    f.writelines(fixed_reqs)

