from sklearn.model_selection import train_test_split
import torch
from torch.utils import data


class UserDataset(data.Dataset):

    def __init__(self, list_of_users, labels, mode='train'):
        self.labels = labels
        self.list_of_users = list_of_users
        X_train, y_train, X_test, y_test = train_test_split(self.list_of_users, self.labels, test_size=0.1,
                                                            random_state=42, shuffle=True)
        if mode == 'train':
            self.list_of_users = X_train
            self.labels = y_train
        else:
            self.list_of_users = X_test
            self.labels = y_test

    def __len__(self):
        'Denotes the total number of samples'
        return len(self.list_of_users)

    def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample
        user_info = self.list_of_users[index]

        # Load data and get label
        X = torch.Tensor(user_info)
        y = torch.Tensor(self.labels[index])

        return X, y
