

"""
========================
V0
========================
"""

from typing import Optional

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next: ListNode = None




class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        if not head:
            return None
        
        if not head.next:
            return head
        
        slow = head
        fast = head.next

        # ERROR：循环条件错误，应该判断快指针是否能继续前进，而非head.next（head永远是头节点，head.next存在则循环无限执行）
        while head.next:
            
            # 条件：快指针跑完全程
            # ERROR：条件顺序错误，应先判断fast是否存在，再判断fast.next（否则fast为None时，fast.next会报空指针异常）
            if not fast.next or not fast:
                return slow

            # ERROR：slow更新逻辑错误，应走一步（slow = slow.next），而非固定指向head.next（永远是第二个节点）
            slow = head.next
            # ERROR：赋值运算符错误（==是比较，=才是赋值）；且fast应基于自身前进两步（fast = fast.next.next），而非head.next.next
            fast == head.next.next


"""
========================
V0 完善版本
========================
"""


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        

        if not head: 
            return None
        if not head.next:
            return head
        
        slow = head
        fast = head.next # ERROR：思维惯性，这里初始化不应该用next，正常初始化，速度不变即可

        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next
        
        return slow
    


"""
========================
V1
========================
"""
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        # 数学归纳法
        if not head:
            return None
        if not head.next:
            return head
        
        slow = head
        fast = head
        
        while fast or fast.next:  # ERROR: 循环条件错误，应为fast and fast.next；
                                  # 用or会导致fast为None时仍进入循环，访问fast.next触发AttributeError
            if fast == None:  # ERROR: 逻辑冗余+位置错误，若循环条件正确，fast不会为None，此判断无意义
                return slow
            
            if fast.next == None:  # ERROR: 判断时机错误，此条件触发时返回slow.next会导致结果错误（如链表[1,2,3,4]会错误返回4而非3）
                return slow.next

            slow = slow.next
            fast = fast.next.next

"""
========================
V1
========================
"""
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        if not head:
            return None
        
        if not head.next:
            return head
        
        slow = head
        fast = head

        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next

        return slow 