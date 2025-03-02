import os
import numpy as np
from random import shuffle

import torch
import torch.optim as optim

from monte_carlo_tree_search import MCTS
from game import AppleGame
from model import AppleGameModel

import time

class Trainer:

    def __init__(self, game: AppleGame, model: AppleGameModel, args):
        self.game = game
        self.model = model
        self.args = args
        self.mcts = MCTS(self.game, self.model, self.args)

    def exceute_episode(self):

        train_examples = []
        state = self.game.get_init_board()

        while True:
            self.mcts = MCTS(self.game, self.model, self.args)
            root = self.mcts.run(self.model, state)

            action_probs = [0 for _ in range(self.game.get_action_size())]
            for k, v in root.children.items():
                action_probs[k] = v.visit_count

            action_probs = action_probs / np.sum(action_probs)
            train_examples.append((state, action_probs))

            action = root.select_action(temperature=0)
            state = self.game.get_next_state(state, action)
            reward = self.game.get_score(state)

            if not self.game.has_legal_moves(state):
                ret: list[list[np.ndarray, np.ndarray, int]] = []
                for hist_state, hist_action_probs in train_examples:
                    # [Board, actionProbabilities, Reward]
                    ret.append((hist_state, hist_action_probs, reward))

                return ret

    def learn(self):
        total_start_time = time.time() 
        for i in range(1, self.args['numIters'] + 1):
            iter_start_time = time.time()
            print("{}/{}".format(i, self.args['numIters']))

            train_examples = []

            eps_start_time = time.time()
            for eps in range(self.args['numEps']):
                iteration_train_examples = self.exceute_episode()
                train_examples.extend(iteration_train_examples)
                if eps % (self.args['numEps'] // 10) == 0:
                    elapsed_eps_time = time.time() - eps_start_time
                    avg_eps_time = elapsed_eps_time / (eps + 1)
                    remaining_eps_time = avg_eps_time * (self.args['numEps'] - eps)
                    print(f"  → Processing: {eps}/{self.args['numEps']} Episode finished "
                        f"(Average {avg_eps_time:.2f}s/Episode, Estimated time left: {remaining_eps_time:.2f}s)")


            shuffle(train_examples)
            
            train_start_time = time.time()
            self.train(train_examples)
            train_duration = time.time() - train_start_time
            print(f"  → Model training completed (Consumed: {train_duration:.2f}s)")
            
            filename = self.args['checkpoint_path']
            self.save_checkpoint(folder=".", filename=filename)

            iter_duration = time.time() - iter_start_time
            avg_iter_time = (time.time() - total_start_time) / i
            remaining_time = avg_iter_time * (self.args['numIters'] - i)
            
            print(f"Iteration {i}/{self.args['numIters']} Completed "
                f"(Consumed time: {iter_duration:.2f}s, Estimated time left: {remaining_time:.2f}s)\n")

    def train(self, examples):
        optimizer = optim.Adam(self.model.parameters(), lr=5e-4)
        pi_losses = []
        v_losses = []

        for epoch in range(self.args['epochs']):
            self.model.train()

            batch_idx = 0

            while batch_idx < int(len(examples) / self.args['batch_size']):
                sample_ids = np.random.randint(len(examples), size=self.args['batch_size'])
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                # predict
                boards = boards.contiguous().cuda()
                target_pis = target_pis.contiguous().cuda()
                target_vs = target_vs.contiguous().cuda()

                # compute output
                out_pi, out_v = self.model(boards)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                pi_losses.append(float(l_pi))
                v_losses.append(float(l_v))

                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

                batch_idx += 1

            print()
            print("Policy Loss", np.mean(pi_losses))
            print("Value Loss", np.mean(v_losses))
            print("Examples:")
            print(out_pi[0].detach())
            print(target_pis[0])

    def loss_pi(self, targets, outputs):
        loss = -(targets * torch.log(outputs)).sum(dim=1)
        return loss.mean()

    def loss_v(self, targets, outputs):
        loss = torch.sum((targets-outputs.view(-1))**2)/targets.size()[0]
        return loss

    def save_checkpoint(self, folder, filename):
        if not os.path.exists(folder):
            os.mkdir(folder)

        filepath = os.path.join(folder, filename)
        torch.save({
            'state_dict': self.model.state_dict(),
        }, filepath)
