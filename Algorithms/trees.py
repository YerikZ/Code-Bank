### Binary Tree Operations
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left 
        self.right = right

def inorder_traversal(root):
    """
    Performs inorder traversal of binary tree (left -> root -> right)
    """
    result = []
    
    def inorder(node):
        if not node:
            return
        inorder(node.left)
        result.append(node.val)
        inorder(node.right)
        
    inorder(root)
    return result

def height_of_bst(node):
    # Base case: if the node is None, return -1
    if node is None:
        return -1
    
    # Recursively find the height of the left and right subtrees
    left_height = height_of_bst(node.left)
    right_height = height_of_bst(node.right)
    
    # The height of the current node is 1 + max of left and right heights
    return 1 + max(left_height, right_height)

def lowest_common_ancestor(root, p, q):
    """
    Finds lowest common ancestor of nodes p and q in binary tree
    """
    if not root or root == p or root == q:
        return root
        
    # Look for p and q in left and right subtrees
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    # If both nodes found in different subtrees, current node is LCA
    if left and right:
        return root
    # If one node found, return that node as potential LCA    
    return left if left else right

def checkBST(root):
    def is_bst(node, min_value, max_value):
        # Base case: an empty node is a valid BST
        if node is None:
            return True
        
        # Check if the current node's value is within the valid range
        if not (min_value < node.value < max_value):
            return False
        
        # Recursively check the left and right subtrees
        return (is_bst(node.left, min_value, node.value) and
                is_bst(node.right, node.value, max_value))
    
    # Start with the full range of valid values
    return is_bst(root, float('-inf'), float('inf'))
# Example usage
if __name__ == "__main__":
    # Create tree:     3
    #                /   \
    #               5     1
    #              / \   / \
    #             6   2 0   8
    #                / \
    #               7   4
    
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)
    
    # Test inorder traversal
    print("Inorder traversal:", inorder_traversal(root))
    
    # Test lowest common ancestor
    p = root.left  # node with value 5
    q = root.left.right.right  # node with value 4
    lca = lowest_common_ancestor(root, p, q)
    print(f"LCA of nodes {p.val} and {q.val} is: {lca.val}")