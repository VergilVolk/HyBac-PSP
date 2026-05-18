#!/usr/bin/env python3
"""从公共数据库下载或本地文件构建参考序列集（模拟）"""
import os

def build_reference():
    # 实际应通过 MEROPS API 或下载文件实现，此处仅展示结构
    print("Building reference sets...")
    base = "data/reference"
    os.makedirs(base, exist_ok=True)
    # 模拟生成空文件或手动放入真实序列
    for f in ["AlkSub.fasta", "AlkLipI4.fasta", "NeuSub.fasta", "NeuLipI4.fasta"]:
        with open(os.path.join(base, f), "w") as fh:
            fh.write(">example\nACDEFGHIKLMNPQRSTVWY\n")
    print("Done. Please replace with real sequences.")

if __name__ == "__main__":
    build_reference()