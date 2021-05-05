from pytorch_lightning.core.saving import get_filesystem, rank_zero_warn
import yaml
from pytorch_lightning.utilities.parsing import AttributeDict

def load_hparams_from_yaml(config_yaml: str):
    fs = get_filesystem(config_yaml)
    if not fs.exists(config_yaml):
        rank_zero_warn(f"Missing Tags: {config_yaml}.", RuntimeWarning)
        return {}

    with fs.open(config_yaml, "r") as fp:
        tags = yaml.full_load(fp)
    return make_attribute_dict(tags)
