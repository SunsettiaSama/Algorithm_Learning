


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        

        # 其实就和438题一样，这里统计一下词频，然后看哈希表是怎么回事

        # 但这里注意，它维护的窗口是动态的
        # 唯一的判定条件就是最短
        # 所以需要针对哈希表来进行维护

        slow_index = 0
        string_frequency_dict = dict()

        # 建立关于t的哈希表
        t_dict = self.build_hash_dict(t)

        res = s

        for fast_index in range(len(s)):
            # 先剪枝
            if fast_index - slow_index + 1 < len(t):
                continue

            # 为当前的区间临时建表
            current_interval_dict = self.build_hash_dict(s[slow_index: fast_index])

            # 比较两个表，如果t_dict是current_interval_dict的子表，则收缩左区间
            while self.compare2dict(current_interval_dict, child_dict = t_dict):
                
                # 记录结果
                if fast_index - slow_index + 1 < len(res):
                    res = s[slow_index: fast_index]

                # 收缩子区间
                slow_index += 1
                current_interval_dict = self.build_hash_dict(s[slow_index: fast_index])
        
        return res


    def build_hash_dict(self, string):

        return_dict = dict()
        for char in string:
            if char not in return_dict:
                return_dict[char] = 1
            else:
                return_dict[char] += 1

        return return_dict
    

    def compare2dict(self, parent_dict, child_dict: dict):

        for key, value in child_dict.items():
            # 词频上来说，一定是parent大于child
            if not (key in parent_dict and parent_dict[key] > child_dict[key]):
                return False

        return True
    
    