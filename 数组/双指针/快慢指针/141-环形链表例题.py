# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next: ListNode = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        
        if not head or not head.next:
            return False
        
        slow = head
        fast = head.next

        while fast and fast.next: 

            if slow == fast:
                return True
            
            slow = slow.next
            fast = fast.next.next
        
        return False




'''
====================
V0
====================
'''

class Solution:
    def hasCycle(self, head: Optional[ListNode]):

        # ERROR:未考虑边界条件,如果输入为空或者单个点,会报错

        slow = head
        fast = head

        while fast and fast.next:

            if slow == fast:  # ERROR: 初始状态slow和fast都指向head，未移动就判断相等，会错误返回True
                return True
            
            slow = slow.next
            fast = fast.next.next

        return False
    




'''
====================
V0 修复版
====================
'''

class Solution:
    def hasCycle(self, head: Optional[ListNode]):

        if not head or not head.next:
            return False
        
        slow = head
        fast = head

        while fast and fast.next:
            
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True
        
        return False


