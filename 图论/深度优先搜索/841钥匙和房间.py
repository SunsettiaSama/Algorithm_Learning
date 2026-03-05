"""
这个题是有向图遍历，问题被定义为：
    如果从节点0出发，是否能遍历图中所有节点

    示例:
    rooms = [[1], [2], [3], []]

    图表示:
    0 → 1 → 2 → 3
    (0号房间有1号房间的钥匙，1号房间有2号房间的钥匙，以此类推)

    rooms = [[1,3], [3,0,1], [2], [0]]

    图表示:
    ↗ 1 ↘
    0       3
    ↘       ↗
    2 ←───
    (更复杂的连接关系，可能存在环)

解法其实很清晰：就是DFS
从0出发，相邻节点就是所谓的key，在外面用一个set来记录访问结果
如果都能成功访问，检查二者长度即可达到要求

"""


class Solution:
    def canVisitAllRooms(self, rooms) -> bool:

        # 这是个图论的题目，是否所有节点都可以访问
        # 图论解决方法主要两种，一种是DFS、一种是BFS

        def explore_room(curr_room_id):
            visited_rooms.add(curr_room_id)

            # 获取指针
            neighbors = rooms[curr_room_id]
            for next_room in neighbors:
                if next_room not in visited_rooms:
                    explore_room(next_room)

        
        visited_rooms = set()
        explore_room(0)

        return len(visited_rooms) == len(rooms)
