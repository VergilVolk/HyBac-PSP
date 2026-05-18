import subprocess
import os
import tempfile
import pandas as pd

def run_hmmsearch(fasta_path, hmm_path, evalue=1e-10, cpus=1):
    """运行 hmmsearch 并返回命中列表 [{id, bit_score, evalue}]"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tbl') as tmp:
        tblout = tmp.name
    try:
        cmd = [
            "hmmsearch",
            "--noali",
            "--cpu", str(cpus),
            "-E", str(evalue),
            "--tblout", tblout,
            hmm_path,
            fasta_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        # 解析 tblout
        hits = []
        with open(tblout) as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.strip().split()
                if len(parts) < 6:
                    continue
                target = parts[0]
                evalue_out = float(parts[4])
                bit_score = float(parts[5])
                hits.append({
                    "id": target,
                    "evalue": evalue_out,
                    "bit_score": bit_score
                })
        return hits
    finally:
        if os.path.exists(tblout):
            os.unlink(tblout)

def normalize_bit_scores(hits, smin=0, smax=2000):
    """将 bit scores 归一化到 [0,1]，smin/smax 建议用参考集自检获得"""
    out = {}
    for hit in hits:
        sid = hit["id"]
        score = hit["bit_score"]
        norm = (score - smin) / (smax - smin) if smax > smin else 0.0
        out[sid] = max(0.0, min(1.0, norm))
    return out