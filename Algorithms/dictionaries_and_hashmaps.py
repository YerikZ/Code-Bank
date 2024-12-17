from collections import defaultdict, Counter
from typing import List

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Groups anagrams together from a list of strings.
    Time complexity: O(n * k) where n is length of strs and k is max length of a string
    Space complexity: O(n)
    """
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Sort characters to use as key - anagrams will have same sorted string
        sorted_str = ''.join(sorted(s))
        anagram_map[sorted_str].append(s)
        
    return list(anagram_map.values())

def contains_duplicate(nums: List[int]) -> bool:
    """
    Determines if array contains any duplicate values.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    seen = set()
    
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
        
    return False

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Returns the k most frequent elements in array.
    Time complexity: O(n log k)
    Space complexity: O(n)
    """
    # Count frequency of each number
    count = Counter(nums)
    
    # Return k numbers with highest frequencies
    return [num for num, _ in count.most_common(k)]

def sherlockAndAnagrams(s):
    # Write your code here
    from collections import defaultdict
    n = len(s)
    substrs = []
    for i in range(n):
        for j in range(i+1, n+1):
            substrs.append(s[i:j])
    # print(substrs)
    anagram_map = defaultdict(int)
    for s in substrs:
        # Sort characters to use as key - anagrams will have same sorted string
        sorted_str = ''.join(sorted(s))
        anagram_map[sorted_str] += 1  
    count = 0
    for c in anagram_map.values():
        count += c * (c-1) // 2 # nC2
    return count

def countTriplets(arr, r):
    # Dictionary to store the potential second and third elements of the triplets
    potential_pairs = {}
    potential_triplets = {}
    count = 0

    for val in arr:
        # If the current value completes any triplet, add those counts
        if val in potential_triplets:
            count += potential_triplets[val]
        
        # If the current value can be the second element in a triplet, 
        # prepare to add it as the third element in future iterations
        if val in potential_pairs:
            if val * r in potential_triplets:
                potential_triplets[val * r] += potential_pairs[val]
            else:
                potential_triplets[val * r] = potential_pairs[val]
        
        # Every element can start a potential pair
        if val * r in potential_pairs:
            potential_pairs[val * r] += 1
        else:
            potential_pairs[val * r] = 1

    return count

def freqQuery(queries):        
    freq_map = {}       # Maps elements to their frequencies
    freq_count_map = {} # Maps frequencies to the count of elements with that frequency
    ans = []

    for operation, value in queries:
        if operation == 1:
            # Insert value
            current_freq = freq_map.get(value, 0)
            new_freq = current_freq + 1
            freq_map[value] = new_freq

            # Update freq_count_map
            if current_freq > 0:
                freq_count_map[current_freq] -= 1
                if freq_count_map[current_freq] == 0:
                    del freq_count_map[current_freq]

            freq_count_map[new_freq] = freq_count_map.get(new_freq, 0) + 1

        elif operation == 2:
            # Delete one occurrence of value
            current_freq = freq_map.get(value, 0)
            if current_freq > 0:
                new_freq = current_freq - 1
                freq_map[value] = new_freq

                # Update freq_count_map
                freq_count_map[current_freq] -= 1
                if freq_count_map[current_freq] == 0:
                    del freq_count_map[current_freq]

                if new_freq > 0:
                    freq_count_map[new_freq] = freq_count_map.get(new_freq, 0) + 1
                else:
                    del freq_map[value]

        elif operation == 3:
            # Check if any element exists with exactly `value` frequency
            ans.append(1 if freq_count_map.get(value, 0) > 0 else 0)

    return ans

# Example usage
if __name__ == "__main__":
    # Test group_anagrams
    strs = ["eat","tea","tan","ate","nat","bat"]
    print("Grouping anagrams:")
    print(f"Input: {strs}")
    print(f"Output: {group_anagrams(strs)}")
    
    # Test contains_duplicate
    nums1 = [1,2,3,1]
    nums2 = [1,2,3,4]
    print("\nChecking for duplicates:")
    print(f"Input: {nums1}")
    print(f"Contains duplicate: {contains_duplicate(nums1)}")
    print(f"Input: {nums2}")
    print(f"Contains duplicate: {contains_duplicate(nums2)}")
    
    # Test top_k_frequent
    nums = [1,1,1,2,2,3]
    k = 2
    print("\nFinding top k frequent elements:")
    print(f"Input: nums = {nums}, k = {k}")
    print(f"Output: {top_k_frequent(nums, k)}")
