# execute_code 替代 terminal 进行外网数据聚合

## 问题

WSL 环境下 `terminal` curl 命令经常超时（30s 硬限制），尤其访问 HN Firebase API、Reddit JSON API 等境外服务时。

## 方案

用 `execute_code` 替代 `terminal` 进行多源并发数据抓取。execute_code 有 5 分钟超时和 Python 原生能力。

## 已验证的 HN 抓取模板

```python
import urllib.request, json

def fetch(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    except Exception as e:
        return {"error": str(e)}

# HN top stories
top = fetch("https://hacker-news.firebaseio.com/v0/topstories.json")
ids = top[:15]
for sid in ids:
    item = fetch(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
    if item and item.get("score", 0) >= 30:
        print(f"[{item['score']}pts] {item['title']}")
```

## 已验证的 Reddit 抓取模板

```python
ml = fetch("https://www.reddit.com/r/MachineLearning/hot.json?limit=10")
for post in ml.get("data", {}).get("children", []):
    d = post["data"]
    print(f"[{d['score']}pts] {d['title']}")
```

## 注意

- HN API 无需认证，无需代理
- Reddit API 走 `.json` 后缀即可绕过 OAuth，但可能被限速
- 始终设 `User-Agent` header，否则 Reddit 返回 429
- 首次请求可能较慢（~20s DNS 解析），但不会像 terminal 那样硬超时
