#!/usr/bin/env python3
"""
LTX2.3 文档集完整性验证脚本
检查 docs/ 目录下的所有文档是否存在且非空
"""

import os
from pathlib import Path

# 预期的文档清单（基于 PLAN_OVERVIEW.md）
EXPECTED_DOCS = [
    "README.md",
    "PLAN_OVERVIEW.md",
    "ACTIVATION_BYPASS.md",
    "SETTINGS_PERSISTENCE.md",
    "LORA_MANAGEMENT_GUIDE.md",
    "WORKFLOW_CONVERSION_TOOL.md",
    "LORA_PRESET_PANEL_API.md",
    "TROUBLESHOOTING.md",
    "CHANGELOG.md",
    "DEVELOPER_HANDBOOK.md"
]

def verify_docs(base_dir):
    """验证文档完整性"""
    docs_dir = Path(base_dir) / "docs"

    print("=" * 60)
    print("  LTX2.3 文档集验证")
    print("=" * 60)
    print()

    if not docs_dir.exists():
        print(f"[ERR] 错误: docs/ 目录不存在: {docs_dir}")
        return False

    all_ok = True
    missing = []
    empty = []

    for doc in EXPECTED_DOCS:
        doc_path = docs_dir / doc

        if not doc_path.exists():
            print(f"[MISS] 缺失: {doc}")
            all_ok = False
            missing.append(doc)
        else:
            size = doc_path.stat().st_size
            if size < 100:  # 文件过小（可能为空或仅标题）
                print(f"[WARN] 过小: {doc} ({size} 字节)")
                empty.append(doc)
            else:
                print(f"[OK] {doc} ({size:,} 字节)")

    print()
    print("=" * 60)

    if all_ok and not empty:
        print("[OK] 验证通过！所有文档存在且非空")
        print(f"   总计: {len(EXPECTED_DOCS)} 个文件")
        return True
    else:
        if missing:
            print(f"[FAIL] 缺失文件: {len(missing)} 个")
            for f in missing:
                print(f"   - {f}")
        if empty:
            print(f"[WARN] 文件过小: {len(empty)} 个")
            for f in empty:
                print(f"   - {f}")
        return False

def check_cross_references():
    """检查文档间的交叉引用"""
    print()
    print("=" * 60)
    print("  交叉引用检查")
    print("=" * 60)
    print()

    docs_dir = Path("D:/LTX2.3_v4.0/docs")
    all_refs = {}

    for doc_file in docs_dir.glob("*.md"):
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # 提取Markdown链接
            import re
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

            internal_refs = []
            for text, href in links:
                # 只检查相对路径的内部引用（不检查 http:// 等外部链接）
                if not href.startswith(('http://', 'https://', 'mailto:', '#')):
                    internal_refs.append(href)

            if internal_refs:
                all_refs[doc_file.name] = internal_refs

    broken_refs = []
    for doc, refs in all_refs.items():
        for ref in refs:
            # 处理 ../ 路径
            ref_path = (docs_dir / ref).resolve()
            if not ref_path.exists():
                broken_refs.append((doc, ref))

    if broken_refs:
        print("[WARN] 发现无效交叉引用:")
        for doc, ref in broken_refs:
            print(f"   {doc} -> {ref}")
    else:
        print("[OK] 所有交叉引用均有效")

    print()

if __name__ == "__main__":
    base = "D:/LTX2.3_v4.0"
    ok = verify_docs(base)

    if ok:
        check_cross_references()
        print("=" * 60)
        print("[OK] 文档集验证完成！")
        print("=" * 60)

        # 统计总字数
        total_chars = 0
        docs_dir = Path(base) / "docs"
        for doc in docs_dir.glob("*.md"):
            with open(doc, 'r', encoding='utf-8') as f:
                content = f.read()
                total_chars += len(content)

        print(f"\n统计信息:")
        print(f"   文档总数: {len(EXPECTED_DOCS)}")
        print(f"   总字符数: {total_chars:,} (~{total_chars//1000}KB)")
        print(f"   预计阅读时间: {total_chars//500} 分钟")
    else:
        print("[FAIL] 验证失败，请检查缺失或过小的文件")
