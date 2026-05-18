import csv
from Bio import SeqIO

def read_fasta(filepath):
    """读取 FASTA 文件，返回字典 {id: str(seq)}"""
    records = SeqIO.parse(filepath, "fasta")
    return {rec.id: str(rec.seq) for rec in records}

def write_csv(filepath, header, rows):
    """写入 CSV 文件"""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

def load_config(config_path="config/default.yaml"):
    import yaml
    with open(config_path) as f:
        return yaml.safe_load(f)