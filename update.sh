git fetch
git reset --hard HEAD
git merge origin/deploy

sudo systemctl restart ferry-planner.service
