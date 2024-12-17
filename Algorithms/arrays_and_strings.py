from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Returns indices of two numbers that add up to target.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    seen = {}  # val -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def find_quadruplet_sum_fast(numbers, target):
    # TODO: Code the same function as above, but faster!
    # Dictionary to store pairwise sums: {sum: [(i, j), ...]}
    pair_sums = {}
    
    n = len(numbers)
    
    # Step 1: Precompute pairwise sums
    for i in range(n):
        for j in range(i + 1, n):  # Ensure i < j to avoid duplicate pairs
            pair_sum = numbers[i] + numbers[j]
            if pair_sum not in pair_sums:
                pair_sums[pair_sum] = []
            pair_sums[pair_sum].append((i, j))
    
    # Step 2: Search for complementary pairs
    for i in range(n):
        for j in range(i + 1, n):  # Ensure i < j
            current_sum = numbers[i] + numbers[j]
            complement = target - current_sum
            
            # Check if complement exists in pair_sums
            if complement in pair_sums:
                for (k, l) in pair_sums[complement]:
                    # Ensure no index is reused
                    # if k != i and k != j and l != i and l != j:
                    return (numbers[i], numbers[j], numbers[k], numbers[l])
    
    return []

def length_of_longest_substring(s: str) -> int:
    """
    Finds length of longest substring without repeating characters.
    Time complexity: O(n)
    Space complexity: O(min(m,n)) where m is size of charset
    """
    char_index = {}  # char -> last index seen
    max_length = 0
    start = 0
    
    for i, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        else:
            max_length = max(max_length, i - start + 1)
        char_index[char] = i
        
    return max_length

def rotate_array(nums: List[int], k: int) -> None:
    """
    Rotates array to right by k steps in-place.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    n = len(nums)
    k = k % n  # Handle case where k > n
    
    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
    
    # Reverse entire array
    reverse(0, n-1)
    # Reverse first k elements
    reverse(0, k-1)
    # Reverse remaining elements
    reverse(k, n-1)


def minimumSwaps(arr):
    n = len(arr)
    # Create a list of tuples where each tuple is (value, index)
    arr_indexed = [(value, index) for index, value in enumerate(arr)]
    
    # Sort the array based on the values
    arr_indexed.sort(key=lambda x: x[0])
    
    # Create a visited array to keep track of visited elements
    visited = [False] * n
    swaps = 0
    
    for i in range(n):
        # If the element is already in the correct position or visited
        if visited[i] or arr_indexed[i][1] == i:
            continue
        
        # Find the size of the cycle
        cycle_size = 0
        j = i
        
        while not visited[j]:
            visited[j] = True
            # Move to the next index
            j = arr_indexed[j][1]
            cycle_size += 1
        
        # If there is a cycle of size k, we need (k - 1) swaps
        if cycle_size > 0:
            swaps += (cycle_size - 1)
    
    return swaps


from collections import Counter
def isValid(s):
    # Count the frequency of each character
    freq_map = Counter(s)
    
    # Count the occurrences of each frequency
    freq_count = Counter(freq_map.values())
    
    if len(freq_count) == 1:
        # All characters have the same frequency
        return "YES"
    elif len(freq_count) == 2:
        # Check if it's valid by removing one character
        keys = list(freq_count.keys())
        if (freq_count[keys[0]] == 1 and (keys[0] - 1 == keys[1] or keys[0] - 1 == 0)) or \
           (freq_count[keys[1]] == 1 and (keys[1] - 1 == keys[0] or keys[1] - 1 == 0)):
            return "YES"
    return "NO"

def rotate_in_place(matrix):
    n = len(matrix)
    # Step 1: Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):  # Start at i+1 to avoid re-swapping
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()

def rotate_in_place(matrix):
    n = len(matrix)
    # Perform a layer-by-layer rotation
    for layer in range(n // 2):
        first = layer
        last = n - layer - 1
        for i in range(first, last):
            # Offset from the layer boundary
            offset = i - first
            
            # Save the top element
            top = matrix[first][i]
            
            # Move left to top
            matrix[first][i] = matrix[last - offset][first]
            
            # Move bottom to left
            matrix[last - offset][first] = matrix[last][last - offset]
            
            # Move right to bottom
            matrix[last][last - offset] = matrix[i][last]
            
            # Move top to right
            matrix[i][last] = top
                    
# Example usage
if __name__ == "__main__":
    # Test two_sum
    nums = [2, 7, 11, 15]
    target = 9
    print("Two Sum:")
    print(f"Input: nums = {nums}, target = {target}")
    print(f"Output: {two_sum(nums, target)}")
    
    # Test length_of_longest_substring
    s = "abcabcbb"
    print("\nLongest Substring Without Repeating Characters:")
    print(f"Input: {s}")
    print(f"Output: {length_of_longest_substring(s)}")
    
    # Test rotate_array
    nums = [1,2,3,4,5,6,7]
    k = 3
    print("\nRotate Array:")
    print(f"Input: nums = {nums}, k = {k}")
    rotate_array(nums, k)
    print(f"Output: {nums}")
