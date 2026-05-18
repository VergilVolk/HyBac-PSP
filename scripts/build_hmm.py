#!/usr/bin/env python3
"""基于参考比对构建 profile HMM"""
import subprocess
import os

def build_hmm(ref_fasta, hmm_out):
    # 先比对
    aln_sto = ref_fasta + ".sto"
    subprocess.run(["mafft", "--auto", ref_fasta], stdout=open(aln_sto, "w"), check=True)
    # 构建 HMM
    subprocess.run(["hmmbuild", hmm_out, aln_sto], check=True)
    # 校准
    subprocess.run(["hmmcalibrate", hmm_out], check=True)
    print(f"HMM built: {hmm_out}")

if __name__ == "__main__":
    build_hmm("data/reference/AlkSub.fasta", "data/hmm/alk_subtilisin.hmm")
    build_hmm("data/reference/AlkLipI4.fasta", "data/hmm/alk_lipase_I4.hmm")