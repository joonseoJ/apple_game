import torch
import torch.nn as nn
import torch.nn.functional as F

class PuzzleNet(nn.Module):
    def __init__(self, input_shape=(10, 17), num_actions=8415):
        super(PuzzleNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * input_shape[0] * input_shape[1], 256)
        
        # Policy head
        self.policy_fc = nn.Linear(256, num_actions)
        
        # Value head
        self.value_fc = nn.Linear(256, 1)
        
    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        
        policy = F.softmax(self.policy_fc(x), dim=-1)  # Probability distribution
        value = torch.tanh(self.value_fc(x))  # Expected outcome
        
        return policy, value

# Test network with random input
def test_model():
    model = PuzzleNet()
    sample_input = torch.rand(1, 10, 17)  # Example game state
    policy, value = model(sample_input)
    print("Policy Output Shape:", policy.shape)  # Should match (1, num_actions)
    print("Value Output Shape:", value.shape)  # Should be (1, 1)

test_model()
