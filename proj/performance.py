import sys
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from markov import identify_speaker
from driver import read_file
    
def time_identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    start = time.perf_counter()
    identify_speaker(speech1, speech2, speech3, k, use_hashtable)
    elapsed = time.perf_counter() - start
    return elapsed

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)

    # add code here to open files & read text
    textA, textB, textC = read_file(filenameA), read_file(filenameB), read_file(filenameC)
    
    # Initialize the pandas DataFrame
    df = pd.DataFrame(columns=['Lines', 'K', 'Run', 'Time'])

    # Perform the timing
    for run in range(1, runs + 1):
        for k in range(1, max_k + 1):
            for implementation in ['hashtable', 'dict']:
                use_hashtable = implementation == 'hashtable'
                elapsed = time_identify_speaker(textA, textB, textC, k, use_hashtable)
                new_row = pd.DataFrame([{
                    'Lines': implementation,
                    'K': k,
                    'Run': run,
                    'Time': elapsed
                }])
                df = pd.concat([df, new_row], ignore_index=True)

    # Plotting the graph and saving img
    plt.figure(figsize=(10, 6))
    sns.pointplot(data=df, x='K', y='Time', hue='Lines',linestyle='-', marker='o')
    plt.title('HashTable vs Python dict')
    plt.ylabel('Average Time (Runs=2)')
    plt.grid(True)
    plt.savefig('..\img\execution_graph.png')