import subprocess
import os

def run_prodigal(fasta_path, output_dir):
    """调用 Prodigal 预测蛋白编码基因（如需）"""
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "prodigal",
        "-i", fasta_path,
        "-a", os.path.join(output_dir, "proteins.faa"),
        "-o", os.path.join(output_dir, "genes.gff"),
        "-p", "meta"  # 宏基因组模式
    ]
    subprocess.run(cmd, check=True)
    return os.path.join(output_dir, "proteins.faa")