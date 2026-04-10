class Solution:
    def sortList(self, head):
        # 创建一个至少两步的链表
        result = [head.val]
        head = head.next
        if result[0] < ？

        # 第零步
        # 返回其本身，可以作为终止条件

        # 第k步
        # 我们已经有了一个列表
        # 那么比较每一个元素，然后实现插入？
        while not head.next == None:
            # 更新一步
            head = head.next
            a0 = head.val
            # 如果下一个值依然存在，则进行处理
            for index in range(len(result)):
                if result[index] < a0 < result[index + 1]:

            
            
        return sorted(head)
    

    