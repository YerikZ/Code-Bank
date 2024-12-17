class LinkedList:
    def __init__(self, data):
        self.data = data
        self.next = None

def view_nodes(head):
    llist = []
    current = head
    while current:
        llist.append(current.data)
        current = current.next    
    return '->'.join(map(str, llist))

def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current 
        current = next_temp
        
    return prev
#current: 1->2->3
#prev: None

#next_temp: 2->3   
#current.next: None => current: 1
#prev: 1
#current: 2->3

#next_temp: 3
#current.next: 1 => current: 2->1
#prev: 2->1
#current: 3

#next_temp: None
#current.next: 2->1 => current: 3->2->1
#prev: 3->2->1
#current: None


def merge_lists(l1, l2):
    dummy = LinkedList(0)
    current = dummy
    
    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
        
    if l1:
        current.next = l1
    if l2:
        current.next = l2
        
    return dummy.next

def has_cycle(head):
    if not head or not head.next:
        return False
        
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
        
    return True

def findMergeNode(head1, head2):
    def get_length(head):
        length = 0
        while head:
            length += 1
            head = head.next
        return length

    # Get the lengths of both linked lists
    len1 = get_length(head1)
    len2 = get_length(head2)
    
    while len1 > len2:
        head1 = head1.next
        len1 -= 1

    while len2 > len1:
        head2 = head2.next
        len2 -= 1

    # Traverse both lists together to find the merge point
    while head1 and head2:
        if head1 == head2:
            return head1.data  # Return the data of the merge node
        head1 = head1.next
        head2 = head2.next

    return None

def insertNodeAtPosition(llist, data, position):
    # Write your code here
    new_node = LinkedList(data)
    
    if position == 0:
        new_node.next = llist
        return new_node
    
    current = llist
    
    for _ in range(position-1):
        if current is None:  
            return llist
        current = current.next
    
    # Insert the new node
    if current is not None:
        new_node.next = current.next  # Point new node to the next node
        current.next = new_node  # Link the previous node to the new node
    
    return llist

# Example usage
if __name__ == "__main__":
    # Create linked list: 1 -> 2 -> 3 -> 4 -> 5
    head = LinkedList(1)
    head.next = LinkedList(2)
    head.next.next = LinkedList(3) 
    head.next.next.next = LinkedList(4)
    head.next.next.next.next = LinkedList(5)

    # Test reverse_list
    print(f"Original: {view_nodes(head)}")
    reversed_head = reverse_list(head)
    print(f"After reversing: {view_nodes(reversed_head)}")

    # Test merge_lists
    # Create two sorted lists
    # l1: 1->3->5
    l1 = LinkedList(1)
    l1.next = LinkedList(3)
    l1.next.next = LinkedList(5)

    # l2: 2->4->6
    l2 = LinkedList(2) 
    l2.next = LinkedList(4)
    l2.next.next = LinkedList(6)

    print("\nMerging lists:")
    print(f"l1: {view_nodes(l1)}")
    print(f"l2: {view_nodes(l2)}")
    merged = merge_lists(l1, l2)
    print(f"Merged list: {view_nodes(merged)}")

    # Test cycle detection
    # Create a list with cycle: 1->2->3->4->2
    cycle_list = LinkedList(1)
    cycle_list.next = LinkedList(2)
    cycle_list.next.next = LinkedList(3)
    cycle_list.next.next.next = LinkedList(4)
    cycle_list.next.next.next.next = cycle_list.next  # Creates cycle

    print("\nCycle detection:")
    print(f"List with cycle: 1->2->3->4->2(cycle)")
    has_cycle = has_cycle(cycle_list)
    print(f"Has cycle: {has_cycle}")
