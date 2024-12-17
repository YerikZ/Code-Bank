class Solution:
    def isValidParentheses(self, s: str) -> bool:
        """
        Determines if string of parentheses is valid
        Time: O(n), Space: O(n)
        """
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        
        for char in s:
            if char in mapping:
                top = stack.pop() if stack else '#'
                if mapping[char] != top:
                    return False
            else:
                stack.append(char)
                
        return not stack

class QueueUsingStacks:
    """
    Implements queue operations using two stacks
    """
    def __init__(self):
        self.stack1 = []  # For push
        self.stack2 = []  # For pop
        
    def push(self, x: int) -> None:
        self.stack1.append(x)
        
    def pop(self) -> int:
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop()
        
    def peek(self) -> int:
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2[-1]
        
    def empty(self) -> bool:
        return len(self.stack1) == 0 and len(self.stack2) == 0

class MinStack:
    """
    Stack supporting push, pop, top and min operations in O(1)
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []
        
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
            
    def pop(self) -> None:
        if self.stack:
            if self.stack[-1] == self.min_stack[-1]:
                self.min_stack.pop()
            self.stack.pop()
            
    def top(self) -> int:
        if self.stack:
            return self.stack[-1]
            
    def getMin(self) -> int:
        if self.min_stack:
            return self.min_stack[-1]

def minimumBribes(q):
    total_bribes = 0
    n = len(q)
    
    for i in range(n):
        # Check if the current position is more than 2 ahead of the original position
        if q[i] - (i + 1) > 2:
            print("Too chaotic")
            return
        
        # Count how many times this person has been bribed
        # We only need to check from max(0, q[i] - 2) to i
        for j in range(max(0, q[i] - 2), i):
            if q[j] > q[i]:
                total_bribes += 1
    
    print(total_bribes)


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
    
# Example usage
if __name__ == "__main__":
    # Test Valid Parentheses
    solution = Solution()
    test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}"]
    print("Valid Parentheses Tests:")
    for s in test_cases:
        print(f"{s}: {solution.isValidParentheses(s)}")
    
    # Test Queue using Stacks
    print("\nQueue using Stacks Tests:")
    queue = QueueUsingStacks()
    queue.push(1)
    queue.push(2)
    print(f"Peek: {queue.peek()}")  # returns 1
    print(f"Pop: {queue.pop()}")    # returns 1
    print(f"Empty: {queue.empty()}")  # returns false
    
    # Test Min Stack
    print("\nMin Stack Tests:")
    minStack = MinStack()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-3)
    print(f"Get Min: {minStack.getMin()}")  # returns -3
    minStack.pop()
    print(f"Top: {minStack.top()}")      # returns 0
    print(f"Get Min: {minStack.getMin()}")  # returns -2
