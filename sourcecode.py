import threading

# Read the input file and split it into a list of words
with open('input_file.txt', 'r') as file:
    data = file.read().split()

# Define the mapper function
def mapper(word):
    return (word, 1)

# Define the reducer function
def reducer(word, counts):
    return (word, sum(counts))

# Create a dictionary to store the intermediate results from the mapper function
intermediate_results = {}

# Define the function to perform the mapping operation for a chunk of data
def map_chunk(chunk):
    for word in chunk:
        if word not in intermediate_results:
            intermediate_results[word] = []
        intermediate_results[word].append(1)

# Define the function to perform the reduce operation for a chunk of data
def reduce_chunk(chunk):
    final_results = {}
    for word in chunk:
        final_results[word] = reducer(word, intermediate_results[word])
    return final_results

# Divide the input data into equal-sized chunks
chunk_size = len(data) // num_threads
chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

# Create a list of threads to perform the mapping operation
threads = []
for chunk in chunks:
    t = threading.Thread(target=map_chunk, args=(chunk,))
    threads.append(t)
    t.start()

# Wait for all the mapping threads to finish
for t in threads:
    t.join()

# Combine the intermediate results from all the threads into a single dictionary
for word in intermediate_results:
    intermediate_results[word] = sum(intermediate_results[word])

# Shuffle the intermediate results by grouping them based on the word
shuffled_results = {}
for word in intermediate_results:
    if intermediate_results[word] not in shuffled_results:
        shuffled_results[intermediate_results[word]] = []
    shuffled_results[intermediate_results[word]].append(word)

# Divide the shuffled data into equal-sized chunks
chunk_size = len(shuffled_results) // num_threads
chunks = [list(shuffled_results.keys())[i:i+chunk_size] for i in range(0, len(shuffled_results), chunk_size)]

# Create a list of threads to perform the reduce operation
threads = []
for chunk in chunks:
    t = threading.Thread(target=reduce_chunk, args=(chunk,))
    threads.append(t)
    t.start()

# Wait for all the reduce threads to finish
for t in threads:
    t.join()

# Combine the final results from all the threads into a single dictionary
final_results = {}
for t in threads:
    for word, count in t.result().items():
        if word
