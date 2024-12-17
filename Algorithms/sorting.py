### Bubble Sort
def bubble_sort(arr):
    if len(arr) <= 1:
        return arr
    
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    
    return arr
    
### Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    
    left = [i for i in arr if i < pivot]
    middle = [i for i in arr if i == pivot]
    right = [i for i in arr if i > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


### Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    return arr

### Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Divide the array
    mid = len(arr) // 2
    # print(mid)
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    # print(mid, left_half, right_half)

    # Merge the sorted halves
    return merge(left_half, right_half)

def merge(left, right):
    sorted_arr = []
    i = j = 0

    # Compare elements from both halves and merge them
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1

    # Append remaining elements, if any
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    # print(f"Sorted {sorted_arr}")
    return sorted_arr

### Count Sort
def count_sort(arr):
    """
    Sort array using counting sort algorithm.
    Time complexity: O(n + k) where k is range of input
    Space complexity: O(k)
    """
    if not arr:
        return arr
        
    # Find range of array elements
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    # Create count array to store count of each unique object
    count = [0] * range_val
    
    # Store count of each object
    for num in arr:
        count[num - min_val] += 1
    
    # Modify count array to store actual positions
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Build output array
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
        
    # Copy output array to arr
    for i in range(len(arr)):
        arr[i] = output[i]
        
    return arr



arr = [1, 5, 2, 4, 3]
print(f"Original: {arr}")

# print("Bubble Sort:")
# print(bubble_sort(arr))

# print("Quick Sort:")
# print(quick_sort(arr))

# print("Merge Sort:")
# print(merge_sort(arr))

print("Insertion Sort:")
print(insertion_sort(arr))