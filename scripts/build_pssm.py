#!/usr/bin/env python3
"""构建 PSSM 矩阵和特征位点筛选"""
import json
import os
import subprocess

def build_pssm(ref_fasta, neutral_fasta, output_json, alignment_out=None):
    # 1. MAFFT 多序列比对
    aln_file = alignment_out or (ref_fasta + ".aln")
    subprocess.run(["mafft", "--auto", ref_fasta], stdout=open(aln_file, "w"), check=True)
    
    # 2. 计算氨基酸频率（简化演示）
    # 实际上需要解析比对，计算每个位点每种氨基酸的观测频率，并与背景频率比较
    # 此处仅生成占位 JSON
    pssm_data = {
        "core_positions": [1, 2, 3],  # 示例位点
        "scores": {
            "1": {"A": 0.5, "R": 1.2},
            "2": {"L": -0.3, "K": 0.8},
            "3": {"S": 0.1, "T": -0.2}
        }
    }
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w") as f:
        json.dump(pssm_data, f, indent=2)
    print(f"PSSM saved to {output_json}")

if __name__ == "__main__":
    build_pssm("data/reference/AlkSub.fasta", "data/reference/NeuSub.fasta", "data/pssm/AlkSub_PSSM.json")
    build_pssm("data/reference/AlkLipI4.fasta", "data/reference/NeuLipI4.fasta", "data/pssm/AlkLipI4_PSSM.json")