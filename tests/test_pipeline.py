import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from api import main
import tempfile

def test_basic():
    # 创建临时输入文件
    with tempfile.NamedTemporaryFile(mode="w", suffix=".fasta", delete=False) as f:
        f.write(">test_protein\nMKKVLALGGL\n")
        input_file = f.name
    output_file = tempfile.mktemp(suffix=".csv")
    try:
        main(input_file, output_file)
        with open(output_file) as out:
            assert "seq_id" in out.readline()
    finally:
        os.unlink(input_file)
        if os.path.exists(output_file):
            os.unlink(output_file)
    print("Test passed.")

if __name__ == "__main__":
    test_basic()