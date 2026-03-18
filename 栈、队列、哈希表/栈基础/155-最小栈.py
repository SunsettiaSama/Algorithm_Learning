class Node:
    """链表节点"""
    def __init__(self, value):
        self.value = value     # 节点值
        self.next = None       # 指向下一个节点的指针
        
class MinStack:
    def __init__(self):
        """初始化空栈"""
        self.top = None        # 栈顶指针，指向链表头节点
    
    def is_empty(self):
        """判断栈是否为空"""
        return self.top is None
    
    def push(self, value):
        """入栈操作 - 在链表头部插入新节点"""
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        """出栈操作 - 删除链表头节点"""
        if self.is_empty():
            raise Exception('栈为空')
        value = self.top.value
        self.top = self.top.next
        return value
    
    def peek(self):
        """查看栈顶元素"""
        if self.is_empty():
            raise Exception('栈为空')
        return self.top.value