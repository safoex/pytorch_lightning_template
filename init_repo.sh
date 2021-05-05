# $1 - repo name
# $2 - shared folder on gdrive
# $3 - venv name [or "venv"]

default_venv_name = "venv"
venv_name = "${2:-$default_venv_name}"

dvc init
dvc add config/config.yaml
git add config/config.yaml.dvc config/.gitignore

if [ -z  "$3" ]
  then
    echo "No gdrive remote folder supplied"
else  
  dvc remote add --default myremote gdrive://$3/$1/dvcstore
fi

mkdir models
mkdir data
mkdir 'test'

mv pytorch_lightning_template $1

python3 -m venv $venv_name
source $venv_name/bin/activate
pip install -r requirements.txt
pip install . -e

#rm init_repo.sh
git add --all
git commit -m 'Initialized repo'
