import json
import subprocess
import tempfile
import os
from Bio import SeqIO, AlignIO

def load_pssm(json_path):
    """加载 PSSM 字典：{位置(1-index): {氨基酸: 分数}} 及核心位点列表"""
    with open(json_path) as f:
        data = json.load(f)
    return data  # 格式 {"core_positions": [idx1, idx2...], "scores": {pos: {aa: score}}}

def align_to_reference(query_fasta, ref_alignment, output_path=None):
    """使用 mafft --add 将查询序列对齐到参考比对，返回临时文件路径"""
    # 需要 MAFFT 已安装
    if output_path is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".aln") as tmp:
            output_path = tmp.name
    cmd = [
        "mafft",
        "--add", query_fasta,
        "--keeplength",  # 保持参考比对的长度
        ref_alignment
    ]
    with open(output_path, "w") as out:
        subprocess.run(cmd, stdout=out, check=True)
    return output_path

def score_sequence(aligned_file, pssm_data, query_id):
    """计算单条序列的 B 分数"""
    alignment = AlignIO.read(aligned_file, "fasta")
    # 查找查询序列在比对中的记录
    query_record = None
    ref_idx_map = {}
    for rec in alignment:
        if rec.id == query_id:
            query_record = rec
        # 保存参考序列的索引（假设参考序列 ID 以 ref_ 开头）
        # 但这里我们只关心比对列，直接遍历列
    if query_record is None:
        return 0.0
    
    core_positions = pssm_data["core_positions"]  # 0-based 或 1-based？这里假设 1-based
    scores_dict = pssm_data["scores"]  # {pos: {aa: score}}
    total = 0
    count = 0
    for pos1 in core_positions:
        pos0 = pos1 - 1  # 转为 0-based
        if pos0 >= len(query_record.seq):
            continue
        aa = query_record.seq[pos0]
        if aa == '-' or aa.upper() not in "ACDEFGHIKLMNPQRSTVWY":
            continue
        aa = aa.upper()
        pos_scores = scores_dict.get(str(pos1), {})
        score = pos_scores.get(aa, 0.0)
        total += score
        count += 1
    if count == 0:
        return 0.0
    return total / count

def score_sequences(fasta_path, pssm_path, ref_alignment, tmp_dir=None):
    """对 FASTA 中所有序列打分，返回 {id: B_score}"""
    pssm = load_pssm(pssm_path)
    # 创建查询 FASTA（与输入相同）
    aligned_file = align_to_reference(fasta_path, ref_alignment)
    results = {}
    # 获取所有查询 ID
    for rec in SeqIO.parse(fasta_path, "fasta"):
        bid = rec.id
        bscore = score_sequence(aligned_file, pssm, bid)
        results[bid] = bscore
    # 清理临时文件
    if tmp_dir is None:
        try:
            os.unlink(aligned_file)
        except:
            pass
    return results