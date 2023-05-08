echo [$(date)]: "START"
echo [$(date)]: "creating environment"
conda create --prefix ./env python=3.7 -y
echo [$(date)]: "activate environment"
source activate ./env
echo [$(date)]: "install requirements"
pip install -r requirements.txt
echo [$(date)]: "export conda environment"
conda env export > conda.yaml
echo "# ${PWD}" > README.md
echo [$(date)]: "first commit"
git init
git remote add origin https://github.com/Sukruth097/dvc-simple-project-template.git
git branch -M main
git add .
git commit -m "first commit"
git push -u origin main
echo [$(date)]: "END"

# to remove everything -
# rm -rf env/ .gitignore conda.yaml README.md .git/