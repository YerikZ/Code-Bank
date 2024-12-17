from typing import List
from heapq import heappush, heappop, heapify
from collections import deque

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def find_kth_largest(nums: List[int], k: int) -> int:
    """
    Find kth largest element in unsorted array using min heap.
    Time complexity: O(n log k)
    Space complexity: O(k)
    """
    # Create min heap of k largest elements
    heap = []
    for num in nums:
        heappush(heap, num)
        if len(heap) > k:
            heappop(heap)
            
    return heap[0]

def merge_k_lists(lists: List[ListNode]) -> ListNode:
    """
    Merge k sorted linked lists into one sorted list using min heap.
    Time complexity: O(N log k) where N is total nodes, k is number of lists
    Space complexity: O(k)
    """
    # Initialize min heap with first node from each list
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heappush(heap, (lst.val, i))
            lists[i] = lst.next
            
    dummy = ListNode(0)
    curr = dummy
    
    # Keep pulling smallest value from heap
    while heap:
        val, i = heappop(heap)
        curr.next = ListNode(val)
        curr = curr.next
        
        if lists[i]:
            heappush(heap, (lists[i].val, i))
            lists[i] = lists[i].next
            
    return dummy.next

class MedianFinder:
    """
    Data structure to find running median.
    Uses two heaps: max heap for lower half, min heap for upper half
    """
    def __init__(self):
        self.small = []  # max heap for lower half
        self.large = []  # min heap for upper half
        
    def addNum(self, num: int) -> None:
        """
        Add number to data structure.
        Time complexity: O(log n)
        """
        # Push to max heap, then move largest to min heap
        heappush(self.small, -num)
        heappush(self.large, -heappop(self.small))
        
        # Balance heaps
        if len(self.large) > len(self.small):
            heappush(self.small, -heappop(self.large))
    
    def findMedian(self) -> float:
        """
        Find median from data structure.
        Time complexity: O(1)
        """
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2

# Example usage
if __name__ == "__main__":
    # Test find_kth_largest
    nums = [3,2,1,5,6,4]
    k = 2
    print("Kth Largest Element:")
    print(f"Input: nums = {nums}, k = {k}")
    print(f"Output: {find_kth_largest(nums, k)}")
    
    # Test MedianFinder
    mf = MedianFinder()
    print("\nMedian Finder:")
    nums = [2,3,4]
    for num in nums:
        mf.addNum(num)
        print(f"After adding {num}, median is {mf.findMedian()}")
