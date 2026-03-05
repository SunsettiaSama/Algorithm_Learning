# 快慢指针核心用法
## 一、概述
快慢指针（双指针的一种）通过两个指针**不同的移动速度/更新频率**遍历数据结构（链表/数组），核心由 `while` 循环驱动，常用于解决环形检测、去重、找中点等问题。

## 二、核心特点
1. **速度可不同**：快慢指针更新步长可差异化（如慢指针走1步、快指针走2步）；
2. **更新可错开**：指针可按逻辑需求错开更新时机（先移动再判断/先判断再移动）；
3. **统一while实现**：所有场景均以 `while` 作为循环核心，通过循环条件控制指针移动边界。
4. **循环终止条件类似**：要么是该数组、链表遍历完成；要么是两指针相遇

## 三、通用模板
```python
def slow_fast_pointer_template(container):
    # 1. 初始化指针（根据场景定初始位置）
    slow = 初始值  # 如数组/链表头节点
    fast = 初始值  # 如数组/链表头节点

    # 2. while循环作为核心驱动（循环条件：指针不越界）
    while 循环边界条件:  # 如fast不越界/快慢指针未相遇
        # 3. 按需执行：先判断/先移动（错开更新频率）
        # 逻辑判断（如元素是否重复/指针是否相遇）
        
        # 4. 差异化更新步长（速度不同）
        slow = slow + 步长1  # 如1步
        fast = fast + 步长2  # 如2步或1步（按需）
    
    # 5. 返回结果（如长度/是否有环/目标位置）
    return 结果
```

## 四、典型示例
### 示例1：环形链表检测（速度不同）
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head):
    if not head or not head.next:
        return False
    
    slow, fast = head, head
    # while循环驱动
    while fast and fast.next:
        # 差异化步长：慢1步、快2步
        slow = slow.next
        fast = fast.next.next
        # 错开更新：先移动再判断
        if slow == fast:
            return True
    return False
```

### 示例2：数组去重（错开更新频率）
```python
def removeDuplicates(nums):
    if not nums:
        return 0
    
    slow, fast = 0, 1
    # while循环驱动
    while fast < len(nums):
        # 错开更新：先判断再移动慢指针
        if nums[slow] != nums[fast]:
            slow += 1  # 慢指针仅在元素不同时更新
            nums[slow] = nums[fast]
        fast += 1  # 快指针持续更新（步长1）
    return slow + 1
```

## 五、核心总结
1. 快慢指针核心是**差异化移动策略**（步长/更新时机），而非固定速度；
2. 所有场景均以 `while` 循环为骨架，循环条件需严格控制指针边界；
3. 更新频率需结合业务逻辑（如去重需“先判断后移动慢指针”，环检测需“先移动后判断”）。