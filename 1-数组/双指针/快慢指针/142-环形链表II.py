
from typing import Optional

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next: ListNode = None

"""
V0

"""  

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        if not head or not head.next:
            return None
        
        slow = head
        fast = head

        while fast and fast.next:
            # ERROR 1：初始slow/fast都指向head，未移动就判断相等，直接break，无论是否有环都提前终止循环
            if slow == fast:
                break
            slow = slow.next
            fast = fast.next.next

        # ERROR 2：未判断是否真的有环（若fast走到链表末尾，说明无环，应直接返回None），无环时仍执行后续逻辑
        slow2 = head
        
        # ERROR 3：循环条件错误，应为「slow != slow2」（直到两指针相遇），而非「slow and slow.next」，会导致提前终止/无效循环
        while slow and slow.next:
            slow = slow.next
            slow2 = slow2.next
            # ERROR 4：判断时机无错，但因循环条件/前置无环判断缺失，实际逻辑无法正确触发
            if slow == slow2:
                return slow
        # ERROR 5：无环时未返回None，函数可能无返回值（违背题目要求）

'''
V0 修复版

'''


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        if not head or not head.next:
            return None
        
        slow = head
        fast = head
        hasCycle = False

        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                hasCycle = True
                break
        
        if not hasCycle:
            return None


        slow2 = head

        while slow != slow2:
            slow = slow.next
            slow2 = slow2.next

        return slow
