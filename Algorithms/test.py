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
        print(f"current: {view_nodes(current)}")
        print(f"prev: {view_nodes(prev)}")        
        
    return prev

# Example usage
if __name__ == "__main__":
    # Create linked list: 1 -> 2 -> 3 -> 4 -> 5
    head = LinkedList(1)
    head.next = LinkedList(2)
    head.next.next = LinkedList(3) 
    # head.next.next.next = LinkedList(4)
    # head.next.next.next.next = LinkedList(5)

    # Test reverse_list
    print(view_nodes(head))
    reversed_head = reverse_list(head)
    print(view_nodes(reversed_head))