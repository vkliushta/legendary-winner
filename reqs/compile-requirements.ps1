pip-compile -o reqs/requirements.txt reqs/requirements.in

pip-compile -o reqs/test-requirements.txt reqs/requirements.txt reqs/test-requirements.in
