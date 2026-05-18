import os
import argparse
from .utils import read_fasta, write_csv, load_config
from .hmm_search import run_hmmsearch, normalize_bit_scores
from .pssm_scorer import score_sequences
from .scoring import compute_cscore, classify

def main(input_fasta, output_csv, config_path="config/default.yaml"):
    config = load_config(config_path)
    alpha = config["alpha"]
    evalue = config["evalue_threshold"]
    high_th = config["cscore_high"]
    medium_th = config["cscore_medium"]

    # 读取所有序列
    seqs = read_fasta(input_fasta)
    print(f"Loaded {len(seqs)} sequences.")

    # HMM 搜索 subtilisin 和 lipase
    all_hits = []
    for hmm_key in ["hmm_subtilisin", "hmm_lipase"]:
        hmm_file = config[hmm_key]
        if not os.path.exists(hmm_file):
            print(f"Warning: HMM file {hmm_file} not found, skipping.")
            continue
        hits = run_hmmsearch(input_fasta, hmm_file, evalue=evalue)
        # 标记来源
        for h in hits:
            h["source"] = hmm_key
        all_hits.extend(hits)
    
    # 去重：同一序列取最高 bit score
    best_hits = {}
    for h in all_hits:
        sid = h["id"]
        if sid not in best_hits or h["bit_score"] > best_hits[sid]["bit_score"]:
            best_hits[sid] = h
    # 归一化 H
    H_scores = normalize_bit_scores(list(best_hits.values()))
    
    # 计算 B 分数（需要参考比对文件）
    # 假设 PSSM 与比对文件在同一位置
    b_scores = {}
    for enzyme_type, pssm_key, ref_aln_key in [
        ("subtilisin", "pssm_subtilisin", "alignment_subtilisin"),
        ("lipase", "pssm_lipase", "alignment_lipase")
    ]:
        pssm_path = config.get(pssm_key)
        ref_aln = config.get(ref_aln_key)
        if not pssm_path or not ref_aln or not os.path.exists(pssm_path):
            continue
        # 这里仅对已经通过 HMM 命中的序列打分（可节省时间）
        relevant_ids = [h["id"] for h in all_hits if h["source"] == f"hmm_{enzyme_type}"]
        if not relevant_ids:
            continue
        # 提取相关序列到临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.fasta') as tmp:
            for rid in relevant_ids:
                if rid in seqs:
                    tmp.write(f">{rid}\n{seqs[rid]}\n")
            tmp_query = tmp.name
        scores = score_sequences(tmp_query, pssm_path, ref_aln)
        b_scores.update(scores)
        os.unlink(tmp_query)
    
    # 综合评分
    results = []
    for sid in seqs:
        H = H_scores.get(sid, 0.0)
        B = b_scores.get(sid, 0.0)
        cs = compute_cscore(H, B, alpha)
        priority = classify(cs, high_th, medium_th)
        results.append([sid, f"{H:.4f}", f"{B:.4f}", f"{cs:.4f}", priority])
    
    # 输出
    header = ["seq_id", "H_score", "B_score", "CScore", "priority"]
    write_csv(output_csv, header, results)
    print(f"Done. Results saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HyBac-PSP: Hydrozyme Bacterial Pre-screen Pipeline")
    parser.add_argument("input", help="Input protein FASTA file")
    parser.add_argument("-o", "--output", default="hybac_results.csv")
    parser.add_argument("--config", default="config/default.yaml")
    args = parser.parse_args()
    main(args.input, args.output, args.config)