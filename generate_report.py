"""
Publication-quality result visualization for mentor presentation.
Run this after main.py to generate enhanced charts.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('results', exist_ok=True)

# Paste your actual round results here from main.py output
round_accuracies = [83.33, 93.86, 96.49, 96.49, 96.49, 96.49, 97.37, 97.37, 97.37, 96.49]
round_losses     = [0.6557, 0.4892, 0.2668, 0.1518, 0.1111, 0.0945, 0.0863, 0.0808, 0.0766, 0.0727]

client_accs = {
    'Client 1 (AWS)':   [84.55, 90.95, 95.36, 95.58, 95.58, 96.91, 98.23, 98.45, 98.45, 97.79],
    'Client 2 (Azure)': [79.25, 87.86, 95.14, 96.03, 96.91, 95.81, 97.35, 97.57, 97.57, 97.57],
    'Client 3 (GCP)':   [69.72, 83.66, 93.03, 94.99, 93.03, 95.86, 94.55, 96.51, 96.51, 94.34],
}

rounds = list(range(1, 11))
colors = ['#2196F3', '#4CAF50', '#FF9800']

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Enhanced DNA Cryptography + Federated Learning\nCloud Data Security Simulation Results',
             fontsize=13, fontweight='bold', y=1.02)

# --- Plot 1: Global Accuracy ---
ax1 = axes[0]
ax1.plot(rounds, round_accuracies, 'b-o', linewidth=2.5, markersize=7, label='Global Model')
ax1.fill_between(rounds, [r - 1.5 for r in round_accuracies],
                          [r + 1.5 for r in round_accuracies], alpha=0.15, color='blue')
ax1.axhline(y=max(round_accuracies), color='green', linestyle='--', alpha=0.6,
            label=f'Peak: {max(round_accuracies):.2f}%')
ax1.set_title('Global Model Accuracy', fontweight='bold')
ax1.set_xlabel('Federated Round')
ax1.set_ylabel('Accuracy (%)')
ax1.set_ylim(75, 100)
ax1.legend()
ax1.grid(True, alpha=0.3)

# --- Plot 2: Global Loss ---
ax2 = axes[1]
ax2.plot(rounds, round_losses, 'r-o', linewidth=2.5, markersize=7)
ax2.fill_between(rounds, round_losses, alpha=0.15, color='red')
ax2.set_title('Global Model Loss', fontweight='bold')
ax2.set_xlabel('Federated Round')
ax2.set_ylabel('Cross-Entropy Loss')
ax2.grid(True, alpha=0.3)

# Add annotation for convergence point
ax2.annotate('Convergence\nbegins', xy=(3, round_losses[2]),
             xytext=(5, 0.35), fontsize=9, color='darkred',
             arrowprops=dict(arrowstyle='->', color='darkred'))

# --- Plot 3: Per-Client Local Accuracy ---
ax3 = axes[2]
for (label, accs), color in zip(client_accs.items(), colors):
    ax3.plot(rounds, accs, '-o', linewidth=2, markersize=6, label=label, color=color)

ax3.set_title('Per-Client Local Accuracy', fontweight='bold')
ax3.set_xlabel('Federated Round')
ax3.set_ylabel('Local Accuracy (%)')
ax3.set_ylim(60, 101)
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/mentor_presentation_results.png', dpi=150, bbox_inches='tight')
print("Saved: results/mentor_presentation_results.png")

# --- Summary Stats Table ---
print("\n" + "="*55)
print("  SUMMARY STATISTICS FOR MENTOR PRESENTATION")
print("="*55)
print(f"  Dataset          : Breast Cancer (Wisconsin)")
print(f"  Num Clients      : 3 (AWS, Azure, GCP simulated)")
print(f"  FL Rounds        : 10")
print(f"  Local Epochs/Round: 3")
print(f"  Initial Accuracy  : {round_accuracies[0]:.2f}%")
print(f"  Peak Accuracy     : {max(round_accuracies):.2f}%")
print(f"  Final Loss        : {round_losses[-1]:.4f}")
print(f"  Convergence Round : 3")
print(f"  DNA Encoding Rules: 8 (per-client unique)")
print(f"  Chaotic Map       : Logistic (r=3.99)")
print(f"  Key Generation    : SHA-256 -> DNA sequence")
print(f"  Encryption Layers : XOR + ADD (double layer)")
print("="*55)
