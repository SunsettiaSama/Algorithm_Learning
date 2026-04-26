
一般的0-1背包问题可以在代码上被写为如下过程

```python 
dp = [inf] * (n+1)
dp[0] = 0
for w, v in items:          # 先遍历物品
    for i in range(w, n+1): # 正序遍历容量
        dp[i] = min(dp[i], dp[i-w] + v)
```


