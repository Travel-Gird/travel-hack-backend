import torch
import torch.nn as nn


class EmbeddingClassifier(nn.Module):

    # define all the layers used in model
    def __init__(self, vocab_size, input_dim=5, embedding_dim=10, output_dim=2, layers=3):
        # Constructor
        super().__init__()

        self.input_dim = input_dim
        self.embedding_dim = embedding_dim

        # embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        # MLP
        mlp_layers = []
        mlp_layers.append(nn.Sequential(
            nn.Linear(input_dim * embedding_dim, input_dim * embedding_dim * 2),
            nn.ReLU(),
            nn.Linear(input_dim * embedding_dim * 2, output_dim))
        )

        self.mlp = nn.Sequential(*mlp_layers)

        # activation function
        self.act = nn.Sigmoid()

    def forward(self, input):
        embedded = self.embedding(input)

        embedded = embedded.reshape(input.size()[0], self.input_dim * self.embedding_dim)

        dense_outputs = self.mlp(embedded)

        # Final activation function
        outputs = self.act(dense_outputs)

        return outputs
