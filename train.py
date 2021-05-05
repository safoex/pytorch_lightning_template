from argparse import ArgumentParser

import pytorch_lightning as pl
import os
#from pytorch_lightning_template.utils.loaders import load_hparams_from_yaml


parser = ArgumentParser(description="Training")
parser.add_argument("--config", type=str, default="./config/config.yaml")
parser.add_argument("--batch_size", type=int, default=32)
parser.add_argument("--num_workers", type=int, default=4)
parser.add_argument("--seed", type=int, default=None)
parser.add_argument("--out", type=str, default="./models/accuracy.pth")
parser.add_argument("--use_tensorboard_logger", type=bool, default=False)

parser = pl.Trainer.add_argparse_args(parser)
arguments = parser.parse_args()

loggers = []

if arguments.use_tensorboard_logger:
    loggers.append(TensorBoardLogger("lightning_logs", name=arguments.dataset_name))

if "MLFLOW_URL" in os.environ.keys():
    print("[train] - Use MLflow logger")
    print("[train] - MLFLOW_URL = {}".format(os.environ["MLFLOW_URL"]))
    print("[train] - MLFLOW_S3_ENDPOINT_URL = {}".format(os.environ["MLFLOW_S3_ENDPOINT_URL"]))
    print("[train] - AWS_ACCESS_KEY_ID = {}".format(os.environ["AWS_ACCESS_KEY_ID"]))
    print("[train] - AWS_SECRET_ACCESS_KEY = {}".format(os.environ["AWS_SECRET_ACCESS_KEY"]))
    loggers.append(MLFlowLogger(experiment_name=arguments.dataset_name,
                                tracking_uri=os.environ["MLFLOW_URL"]))

logger = LoggerCollection(loggers)

# Seed
deterministic = False
seed = 0
if arguments.seed is not None:
    pl.seed_everything(arguments.seed)
    deterministic = True
    seed = arguments.seed

# Make trainer
params = load_hparams_from_yaml(arguments.config)
checkpoint_callback = pl.callbacks.ModelCheckpoint(filepath=arguments.out)
trainer = pl.Trainer.from_argparse_args(arguments, logger=logger, callbacks=[checkpoint_callback],
                                        deterministic=deterministic, max_epochs=params.max_epochs,
                                        profiler="simple")

# Make data module
data_module_params = params.data_module
# ...

# Load parameters
model_params = params.model
model_params.data_module = data_module_params
print("Load model from params \n" + str(model_params))

# Make model
model = ModelFactory().make_model(model_params)

print("Start training")
trainer.fit(model, data_module)

