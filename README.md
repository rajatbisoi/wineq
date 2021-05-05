create env
'''
conda create -n winequality python=3.7 -y
'''


activate env
'''
conda activate winequality
'''


created a requirements file

and installed requirements
'''
pip install -r requirements.txt
'''


downlaod wine data from kaggle



git init

dvc init
dvc add data_given\winequality.csv

git add .
git commit -m "first commit"
git remote add origin https://github.com/rajatbisoi/wineq.git
git push origin master

# one liner update
  git add . && git commit -m "commit"


dvc repo
dvc metrics diff
dvc socres show

tox command -
'''bash
tox
'''
for rebuilding -
'''bash
tox -r 
'''
pytest command
'''bash
pytest -v
'''

setup commands -
'''bash
pip install -e . 
'''

build your own package commands- 
'''bash
python setup.py sdist bdist_wheel
'''




