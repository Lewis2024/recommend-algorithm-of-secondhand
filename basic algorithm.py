from scipy.stats import pearsonr

# 待预测的用户i的商品互动表，2表示用户收藏且购买了商品，1表示用户购买或收藏了商品，0表示用户没有购买或收藏商品
i = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# 商品互动表
lists = [
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # j用户
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # k用户
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],  # l用户
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # m用户
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],  # n用户
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # o用户
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],  # p用户
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # q用户
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],  # r用户
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 1]   # s用户
]

# 首先求i与其他用户的皮尔逊相关系数
# 然后根据皮尔逊相关系数和其他用户的商品互动表，预测用户i对每一个商品的评分
s = [0 for _ in range(len(i))]
R = [0 for _ in range(len(i))]
for list in lists:
    correlation, _ = pearsonr(i, list)
    r = [correlation * item for item in list]
    s = [s_item + correlation for s_item in s]
    mean_list = sum(list)/len(list)
    R = [(R_item + (r_item - mean_list) * correlation) for R_item, r_item in zip(R, r)]

mean_i = sum(i)/len(i)

print([mean_i + R_item/abs(s_item) for R_item, s_item in zip(R, s)])