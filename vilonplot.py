import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def read_data_file(filename):
    """Read a file with numeric values, one per line."""
    with open(filename, 'r') as f:
        data = [float(line.strip()) for line in f if line.strip()]
    return data

def create_violin_plot(minicore_file, compositecore_file, output_file="violin_plot.png"):
    """Create a violin plot comparing data from two files."""
    
    # Read data from files
    try:
        minicore_data = read_data_file(minicore_file)
        compositecore_data = read_data_file(compositecore_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Error reading files: {e}")
        return
    
    # Create a DataFrame in the format required by seaborn
    df = pd.DataFrame({
        'Dataset': ['Minicore'] * len(minicore_data) + ['Compositecore'] * len(compositecore_data),
        'Value': minicore_data + compositecore_data
    })
    
    # Set up the figure
    plt.figure(figsize=(10, 6))
    
    # Create violin plot
    sns.violinplot(x='Dataset', y='Value', data=df, inner='box', palette='pastel')
    
    # Add individual data points
    sns.stripplot(x='Dataset', y='Value', data=df, size=4, color='.3', alpha=0.7)
    
    # Add statistics
    for i, dataset in enumerate(['Minicore', 'Compositecore']):
        data = minicore_data if i == 0 else compositecore_data
        plt.text(i, max(data) + 0.01, f"n={len(data)}", ha='center')
        plt.text(i, min(data) - 0.03, f"mean={np.mean(data):.4f}", ha='center')
    
    # Customize plot
    plt.title('Distribution Comparison: Minicore vs Compositecore', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel('Value', fontsize=12)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Violin plot saved as {output_file}")
    
    # Display the plot
    plt.show()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 3:
        minicore_file = sys.argv[1]
        compositecore_file = sys.argv[2]
        
        output_file = "violin_plot.png"
        if len(sys.argv) >= 4:
            output_file = sys.argv[3]
            
        create_violin_plot(minicore_file, compositecore_file, output_file)
    else:
        print("Usage: python script.py minicore_file compositecore_file [output_file]")
        print("Example: python script.py Minicore Compositecore violin_plot.png")
