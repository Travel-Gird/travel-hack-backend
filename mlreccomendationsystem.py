import os
import time

import torch
import yaml

from sklearn.metrics import accuracy_score

from src.loader import UserDataset
from src.model import EmbeddingClassifier
import db


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = .0
        self.avg = .0
        self.sum = .0
        self.count = .0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class MLPlaceRecommendation:
    """
    Places recommendation system

    """

    def __init__(self, config='config.yaml'):
        """
        :param config: type(string) .yaml file with parameters for model
        """
        self.root_path = os.path.realpath(__file__)
        config_path = os.path.join(self.root_path, config)
        self.__config = self.config_load(config_path)
        self.best_model_path = self.get_best_model_path()
        self.model = EmbeddingClassifier(1000)
        self.device = torch.device("cuda:0")

    @staticmethod
    def config_load(config_path: str):
        """
        Config loader.

        :param config_path: type(string) path to config file, it recommended to be inside the root folder
        :return: type(dict) config with model parameters
        """
        with open(config_path) as c_file:
            config = yaml.safe_load(c_file)
        return config

    def get_best_model_path(self):
        """
        Best model path loader from folder - 'weights'
        :return: type(string) Path to best model, without root
        """
        weights_paths = os.listdir(os.path.join(self.root_path, 'weights'))
        self.scores = [path.split('_').split('.') for path in weights_paths]
        best_model_path = f'weights/model_score_{max(self.scores)}.pth'
        self.model.load_state_dict(torch.load(best_model_path))

    def predict(self, data):
        self.best_model_path()
        self.model.eval()
        with torch.no_grad():
            output = self.model(torch.Tensor([data]).to(self.device))
            output = output.float()
        return output.data

    @staticmethod
    def accuracy(output, target):
        """Computes the accuracy over the k top predictions for the specified values of k"""
        with torch.no_grad():
            output = torch.argmax(output, dim=1).cpu().detach().numpy()
            target = target.cpu().detach().numpy()
            return [accuracy_score(output, target)]

    @staticmethod
    def get_list_from_db():
        return db.get_data_for_study()

    def train(self):
        usr_info, labels = self.get_list_from_db()
        training_set = UserDataset(usr_info, labels, mode='train')
        valid_set = UserDataset(usr_info, labels, mode='valid')

        train_loader = torch.utils.data.DataLoader(training_set, batch_size=64, shuffle=True, num_workers=4)
        val_loader = torch.utils.data.DataLoader(valid_set, batch_size=64, num_workers=2)

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3,
                                                               verbose=False)

        log_interval = self.__config['log_interval']
        max_epoch = self.__config['MAX_EPOCH']
        n_rounds = self.__config['n_rounds']

        k = 0
        best_score = 0

        for epoch in range(1, max_epoch):

            batch_time = AverageMeter()
            losses = AverageMeter()
            top1 = AverageMeter()

            end = time.time()

            self.model.train()
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(self.device), target.to(self.device)
                optimizer.zero_grad()
                output = self.model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()

                output = output.float()
                loss = loss.float()

                # measure accuracy and record loss
                acc1 = self.accuracy(output.data, target)[0]
                losses.update(loss.item(), data.shape[0])
                top1.update(acc1.item(), data.shape[0])

                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()

                if batch_idx % log_interval == 0:
                    print('Epoch: [{0}][{1}/{2}]\t'
                          'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                          'Acc@1 {top1.val:.3f} ({top1.avg:.3f})'.format(
                        epoch, batch_idx, len(train_loader), batch_time=batch_time,
                        loss=losses, top1=top1))

            batch_time = AverageMeter()
            losses_validation = AverageMeter()
            top1_validation = AverageMeter()

            end = time.time()

            self.model.eval()
            with torch.no_grad():
                for batch_idx, (data, target) in enumerate(val_loader):
                    data, target = data.to(self.device), target.to(self.device)

                    # compute output
                    output = self.model(data)
                    loss = criterion(output, target)

                    output = output.float()
                    loss = loss.float()

                    # measure accuracy and record loss
                    acc1 = self.accuracy(output.data, target)[0]
                    losses_validation.update(loss.item(), data.shape[0])
                    top1_validation.update(acc1.item(), data.shape[0])

                    # measure elapsed time
                    batch_time.update(time.time() - end)
                    end = time.time()

                    if batch_idx % log_interval == 0:
                        print('Validation: [{0}][{1}/{2}]\t'
                              'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                              'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                              'Acc@1 {top1.val:.3f} ({top1.avg:.3f})'.format(epoch,
                                                                             batch_idx, len(val_loader),
                                                                             batch_time=batch_time,
                                                                             loss=losses_validation,
                                                                             top1=top1_validation))
            scheduler.step(losses.avg)

            print('* Epoch {0} \t'
                  'Acc@1 {top1.avg:.3f}'.format(epoch,
                                                top1=top1_validation))

            if top1_validation.avg > best_score:
                best_score = top1_validation.avg
                best_filename = f'weights/model_score_{best_score}.pth'
                self.save_model(self.model.state_dict(), filename=best_filename)

                k = 0
            elif k < n_rounds:
                k += 1
            elif k == n_rounds:
                break

    def save_model(self, state, filename):
        """
        Save the training model
        """
        torch.save(state, filename)
