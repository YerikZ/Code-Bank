from typing import List

def climb_stairs(n: int) -> int:
    """
    Calculate number of distinct ways to climb n stairs, taking 1 or 2 steps at a time.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if n <= 2:
        return n
        
    # Only need to store previous two values
    one_step = 1  # Ways to climb 1 stair
    two_steps = 2 # Ways to climb 2 stairs
    
    for i in range(3, n + 1):
        curr = one_step + two_steps
        one_step = two_steps
        two_steps = curr
        
    return two_steps

def longest_increasing_subsequence(nums: List[int]) -> int:
    """
    Find length of longest strictly increasing subsequence.
    Time complexity: O(n^2)
    Space complexity: O(n)
    """
    if not nums:
        return 0
        
    # dp[i] represents length of LIS ending at index i
    dp = [1] * len(nums)
    
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                
    return max(dp)

def coin_change(coins: List[int], amount: int) -> int:
    """
    Find minimum number of coins needed to make given amount.
    Time complexity: O(amount * len(coins))
    Space complexity: O(amount)
    """
    # Initialize dp array with amount + 1 (impossible value)
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    return dp[amount] if dp[amount] != amount + 1 else -1

# Example usage
if __name__ == "__main__":
    # Test climb_stairs
    n = 5
    print("Climbing Stairs:")
    print(f"Input: n = {n}")
    print(f"Output: {climb_stairs(n)}")
    
    # Test longest_increasing_subsequence
    nums = [10,9,2,5,3,7,101,18]
    print("\nLongest Increasing Subsequence:")
    print(f"Input: nums = {nums}")
    print(f"Output: {longest_increasing_subsequence(nums)}")
    
    # Test coin_change
    coins = [1,2,5]
    amount = 11
    print("\nCoin Change:")
    print(f"Input: coins = {coins}, amount = {amount}")
    print(f"Output: {coin_change(coins, amount)}")
