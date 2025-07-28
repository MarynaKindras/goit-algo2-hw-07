import time
import random
from collections import OrderedDict
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)


# Custom LRU Cache implementation
class LRUCache:
    def __init__(self, maxsize):
        self.cache = OrderedDict()
        self.maxsize = maxsize

    def get(self, key):
        if key in self.cache:
            # Move the key to the end to mark it as recently used
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def set(self, key, value):
        if key in self.cache:
            # Update the value and move the key to the end
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            # Remove the oldest item if the cache is full
            self.cache.popitem(last=False)


# Function to calculate the sum of elements in a range without using a cache
def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])


# Function to update an element in the array without using a cache
def update_no_cache(array, index, value):
    array[index] = value


# Function to calculate the sum of elements in a range using an LRU cache
def range_sum_with_cache(array, L, R, cache):
    key = (L, R)
    cached_result = cache.get(key)
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R + 1])
    cache.set(key, result)
    return result


# Function to update an element in the array and invalidate the cache
def update_with_cache(array, index, value, cache):
    array[index] = value
    # Remove all cached results that depend on the updated index
    keys_to_remove = [key for key in cache.cache if key[0] <= index <= key[1]]
    for key in keys_to_remove:
        del cache.cache[key]


# Generate a random array and a list of queries
def generate_data(N, Q):
    array = [random.randint(1, 100) for _ in range(N)]
    queries = []
    for _ in range(Q):
        if random.random() < 0.5:
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))
    return array, queries


# Main function to test the performance
def main():
    N = 100_000
    Q = 50_000
    array, queries = generate_data(N, Q)

    # Test without cache
    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(array, query[1], query[2])
        else:
            update_no_cache(array, query[1], query[2])
    no_cache_time = time.time() - start_time

    # Test with LRU cache
    cache = LRUCache(maxsize=1000)
    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(array, query[1], query[2], cache)
        else:
            update_with_cache(array, query[1], query[2], cache)
    cache_time = time.time() - start_time

    # Calculate the speedup
    speedup = no_cache_time / cache_time if cache_time != 0 else 0

    # Print the results
    print(
        Fore.GREEN + f"Execution time without caching: {no_cache_time:.2f} seconds")
    print(
        Fore.BLUE + f"Execution time with LRU cache: {cache_time:.2f} seconds")
    print(Fore.YELLOW + f"Speedup with caching: {speedup:.2f}x")


if __name__ == "__main__":
    main()
