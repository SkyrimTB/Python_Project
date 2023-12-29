import sys
from markov import identify_speaker

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)
    if hashtable_or_dict == "hashtable":
        use_hashtable = True
    else:
        use_hashtable = False

    # add code here to open files & read text
    textA, textB, textC = read_file(filenameA), read_file(filenameB), read_file(filenameC)
    
    # add code to call identify_speaker & print results
    prob_A, prob_B, most_likely_speaker = identify_speaker(textA, textB, textC, k, use_hashtable)

    # Format and print the output
    print(f"Speaker A: {prob_A}")
    print(f"Speaker B: {prob_B}\n")
    print(f"Conclusion: Speaker {most_likely_speaker} is most likely")

    # Output should resemble (values will differ based on inputs):

    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    # Conclusion: Speaker A is most likely
