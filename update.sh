git fetch --all
git reset --hard origin/main

. .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-prod.txt

sudo systemctl restart ferry-planner.service
