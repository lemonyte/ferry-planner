git fetch
git reset --hard HEAD
git merge

source .venv/bin/activate
pip install -r requirements.txt
pip install uvicorn[standard]

sudo systemctl restart ferry-planner.service
