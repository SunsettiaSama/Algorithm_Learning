


import sys

def get_input():

    lines = sys.stdin.read().strip().split('\n')
    lines = iter(lines)

    # 直播内容数和查询条数
    total_nums, query_nums = list(map(int, next(lines).split(" ")))

    contexts = []
    for i in range(total_nums):
        contexts.append(tuple(map(int, next(lines).split(" "))))
    
    result_queries = []
    for i in range(query_nums):
        result_queries.append( int(next(lines)) )
    
    return total_nums, query_nums, contexts, result_queries

def isLarger(x, y):
    # x,y = (内容ID,主播ID,点赞,评论,时间)
    if x[2] != y[2]: return x[2] > y[2]
    if x[3] != y[3]: return x[3] > y[3]
    if x[4] != y[4]: return x[4] < y[4]
    return x[0] < y[0]

def main():


    total_nums, query_nums, contexts, result_queries = get_input()

    # 使用哈希表来存储检索结果，每个都只检索一遍，并且进行排名
    # 一边存储一边计算，然后把所有的值在最后重新分配

    # 哈希表的话还需要建表，能不能直接算出来呢？
    # 算了，就正常的哈希表吧
    rank_dict = dict()
    for context_index in range(total_nums):

        # 最好以主播索引为键
        condition_tuple = contexts[context_index]
        curr_idx = condition_tuple[0]
        curr_condition = contexts[context_index] + [context_index]

        # 没有主播信息
        if not curr_idx in rank_dict:
            rank_dict[curr_idx] = curr_condition
        # 有该主播信息，去重
        else:
            old_condition = rank_dict[curr_idx]
            # 判断可行，那么就更新主播列表
            if isLarger(curr_condition, old_condition):
                rank_dict[curr_idx] = curr_condition
    
    # 这样就排序完成了
    host_list = rank_dict.values()
    sorted_host_list = sorted(host_list, lambda x: (-x[1], -x[2], x[3], x[0]))
    rank_indices = 


    # 接下来对剩下的内容进行排序

    
    # 这样就拿到了有效的哈希表
    # 逻辑不清晰






    return 



    