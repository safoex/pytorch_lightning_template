from argparse import ArgumentParser

import torch
import pytorch_lightning as pl
from pytorch_lightning.metrics.functional import accuracy
from torch.nn import functional as F


class LitClassifier(pl.LightningModule):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        # ...
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        result = pl.TrainResult(minimize=loss)
        result.log('train_loss', loss)
        return result

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        result = pl.EvalResult(checkpoint_on=loss)
        result.log('val_loss', loss)
        result.log('val_acc', accuracy(y_hat, y))
        return result

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        result = pl.EvalResult(checkpoint_on=loss)
        result.log('test_loss', loss)
        result.log('test_acc', accuracy(y_hat, y))
        return result

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)


class LitDataModule(pl.LightningDataModule):
    def __init__(self):
        super().__init__()
        # ...

    def setup(self, stage=None):
        # self.dataset.load_dataset(self.dataset_folder)
        pass

    def train_dataloader(self) -> DataLoader:
        # return DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True, num_workers=self.num_workers)
        pass


def cli_main():
    pl.seed_everything(1234)

    # args
    parser = ArgumentParser()
    parser.add_argument('--gpus', default=0, type=int)

    # optional... automatically add all the params
    # parser = pl.Trainer.add_argparse_args(parser)
    # parser = MNISTDataModule.add_argparse_args(parser)
    args = parser.parse_args()

    # data
    # mnist_train, mnist_val, test_dataset = mnist()

    # model
    # model = LitClassifier(**vars(args))

    # training
    trainer = pl.Trainer(gpus=args.gpus, max_epochs=2, limit_train_batches=200)
    # trainer.fit(model, mnist_train, mnist_val)

    # trainer.test(test_dataloaders=test_dataset)


if __name__ == '__main__':  # pragma: no cover
    cli_main()