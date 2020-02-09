import os
import time

import torch
import yaml

import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

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
        self.root_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
        config_path = os.path.join(self.root_path, config)
        print(config_path)
        self.__config = self.config_load(config_path)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else 'cpu')
        self.is_model_trained = False
        self.model = EmbeddingClassifier(self.__config['reccomendation_alg_params']['vocab_size'])
        self.model = self.model.to(self.device)
        self.load_best_model()

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

    def load_best_model(self):
        """
        Best model path loader from folder - 'weights'
        :return: type(string) Path to best model, without root
        """
        weights_paths = os.listdir(os.path.join(self.root_path, 'weights'))
        self.scores = [int(path.split('_')[2].split('.')[0]) for path in weights_paths]
        best_model_path = f'weights/model_score_{max(self.scores)}.pth'
        self.model.load_state_dict(torch.load(best_model_path))

    def predict(self, data):
        self.load_best_model()
        self.model.eval()
        data = np.array(data)
        enc = LabelEncoder()
        data[:, 0] = enc.fit_transform(data[:, 0])
        data[:, 3] = enc.fit_transform(data[:, 3])
        with torch.no_grad():
            output = self.model(torch.LongTensor(data).to(self.device))
            output = output.float()
        return output.cpu().detach().numpy()[:, 1]

    @staticmethod
    def accuracy(output, target):
        """Computes the accuracy over the k top predictions for the specified values of k"""
        with torch.no_grad():
            output = torch.argmax(output, dim=1).cpu().detach().numpy()
            target = target.cpu().detach().numpy()
            return [accuracy_score(output, target)]

    @staticmethod
    def get_list_from_db():
        enc = LabelEncoder()
        data = db.get_data_for_study()
        labels = data[:, -1]
        data = data[:, :-1]
        data[:, 0] = enc.fit_transform(data[:, 0])
        data[:, 3] = enc.fit_transform(data[:, 3])
        return data, labels

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

        log_interval = self.__config['reccomendation_alg_params']['log_interval']
        max_epoch = self.__config['reccomendation_alg_params']['MAX_EPOCH']
        n_rounds = self.__config['reccomendation_alg_params']['n_rounds']

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
        self.is_model_trained = True

    def save_model(self, state, filename):
        """
        Save the training model
        """
        torch.save(state, filename)


if __name__ == '__main__':
    ml_model = MLPlaceRecommendation()
    test = [[np.random.randint(1, 100), np.random.randint(16, 60), np.random.randint(0, 2), np.random.randint(1, 100),
             np.random.randint(1, 100)] for i in range(16)]
    ml_model.predict(test)
