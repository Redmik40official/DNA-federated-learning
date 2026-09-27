import torch
import torch.nn as nn
import torch.optim as optim

class ThreatToDNAModel(nn.Module):
    def __init__(self, input_dim=4):
        super(ThreatToDNAModel, self).__init__()
        # Input features: CPU load, failed logins, network traffic, latency
        self.fc1 = nn.Linear(input_dim, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 8)
        
        # We output to two different heads
        # Head 1: Predict Mapping Rule (4 classes: 0, 1, 2, 3)
        self.rule_head = nn.Linear(8, 4)
        
        # Head 2: Predict Key Length (4 classes: 0=128, 1=256, 2=512, 3=1024)
        self.length_head = nn.Linear(8, 4)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        
        rule_logits = self.rule_head(x)
        length_logits = self.length_head(x)
        
        return rule_logits, length_logits

# Helper function to convert prediction to actual key length
def get_key_length_from_prediction(pred_class):
    mapping = {0: 128, 1: 256, 2: 512, 3: 1024}
    return mapping.get(pred_class, 128)

if __name__ == "__main__":
    # Test the model structure
    model = ThreatToDNAModel()
    # Dummy input: 1 sample, 4 features
    dummy_input = torch.tensor([[45.0, 5.0, 500.0, 50.0]])
    rule_pred, length_pred = model(dummy_input)
    
    print("Model initialized successfully.")
    print(f"Rule Logits: {rule_pred}")
    print(f"Length Logits: {length_pred}")
