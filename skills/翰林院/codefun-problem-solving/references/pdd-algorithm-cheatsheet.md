# PDD 笔试算法模板速查

Full template file: `/mnt/d/hermes_output/20260516/PDD_algorithm_cheatsheet.py`
Last updated: 2026-05-16

## 50+ 模板覆盖 12 大类

| # | 模块 | 核心模板 |
|---|------|---------|
| 一 | 数据结构 | Fenwick Tree, DSU, 单调栈 |
| 二 | 二分 | 标准/左边界/旋转数组/二分答案(运包裹) |
| 三 | 排序 | 快排/快选(第K大)/归并/堆排 |
| 四 | DP | 01背包/完全/LIS/LCS/回文/编辑距离/打家劫舍/零钱 |
| 五 | 贪心 | 区间合并/区间最大匹配/跳跃游戏II |
| 六 | 滑动窗口 | 最长无重复/最小覆盖/盛水/三数之和 |
| 七 | 树 | 数组LCA/TreeNode LCA/路径和III/序列化 |
| 八 | 图 | BFS最短路/拓扑排序/岛屿 |
| 九 | 字符串 | KMP/大数加减 |
| 十 | 前缀和 | 一维/二维/差分数组 |
| 十一 | 数学 | 快速幂/GCD/位运算/素数筛/组合数 |
| 十二 | 链表 | 反转/环检测/合并 |

## 记忆要点

- **01背包倒序，完全背包正序** ← 最容易写反
- **二分答案**: `left=max`, `right=sum`, `while left<right`, `can(mid) → right=mid else left=mid+1`
- **旋转数组**: 先判 `nums[l]<=nums[m]` 定左半有序
- **数组存树LCA**: `while p!=q: 大的//=2` ← 一行流
- **快选第K大**: `target = len(nums)-k`, partition + 递归
- **差分数组**: `diff[l]+=val; diff[r+1]-=val`，最后前缀和还原
- **拓扑排序**: BFS入度法，`len(res)==n` 判无环
