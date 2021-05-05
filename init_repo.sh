# $1 - repo name
# $2 - shared folder on gdrive
# $3 - venv name [or "venv"]

DEFAULT_VENV_NAME="venv"
VENV_NAME="${2:-$DEFAULT_VENV_NAME}"
echo $VENV_NAME

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

#rm init_repo.sh
git add --all
git commit -m 'Initialized repo'

python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate
pip install -r requirements.txt
pip install . -e


