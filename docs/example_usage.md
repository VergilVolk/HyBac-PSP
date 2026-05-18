# Example Usage

```bash
# 构建参考集（需手动提供真实序列）
python scripts/build_reference.py
# 构建 PSSM
python scripts/build_pssm.py
# 构建 HMM
python scripts/build_hmm.py
# 运行预筛选
python src/api.py example_input.fasta -o results.csv