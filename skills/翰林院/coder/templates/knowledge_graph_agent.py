#!/usr/bin/env python3
"""
Knowledge Graph Agent — 双引擎架构模板
ChromaDB 向量检索 + NetworkX 知识图谱 + LLM 实体关系抽取

适用场景：
- 从非结构化日志/文本中抽取实体关系构建知识图谱
- LLM 驱动的语义检索 + 图推理融合
- 面试展示：evidence 可追溯、降级策略、增量更新

依赖: pip install chromadb sentence-transformers networkx openai
"""

# 完整源码见 /mnt/d/hermes_output/knowledge_graph_agent.py
# 核心架构：
#   EntityExtractor (LLM + regex fallback)
#   RelationExtractor (LLM triplet + fallback co-type association)
#   VectorStore (ChromaDB + sentence-transformers)
#   GraphStore (NetworkX DiGraph + PageRank + BFS)
#   HybridRetriever (score = α·cosine + (1-α)·pagerank)
