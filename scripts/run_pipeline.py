#!/usr/bin/env python3
"""一键运行完整预筛选流程"""
import sys
sys.path.insert(0, "src")
from api import main

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_fasta")
    parser.add_argument("-o", "--output", default="results.csv")
    parser.add_argument("--config", default="config/default.yaml")
    args = parser.parse_args()
    main(args.input_fasta, args.output, args.config)