echo [$(date)]: "START"
echo [$(date)]: "creating environment"
conda create -p venv python=3.7 -y
echo [$(date)]: "activate environment"
source activate venv/

echo [$(date)]: "install requirements"
pip install -r requirements.txt
echo [$(date)]: "export conda environment"
conda env export > conda.yaml
echo "# ${PWD}" > README.md
echo [$(date)]: "first commit"
# git init
# git remote add origin https://github.com/Sukruth097/dvc-simple-project-template.git
# git branch -M main
# git add .
# git commit -m "first commit"
# git push -u origin main
echo [$(date)]: "END"

# to remove everything -
# rm -rf venv/ .gitignore conda.yaml README.md .git/