# HyBac-PSP

<p align="center">
  <b>Hy</b>drozyme <b>Bac</b>terial <b>P</b>re-<b>S</b>creen <b>P</b>ipeline<br>
  <i>面向碱性水解酶产生菌的计算预筛选工具</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="version">
  <img src="https://img.shields.io/badge/python-≥3.8-green" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-orange" alt="license">
  <img src="https://img.shields.io/badge/HMMER-3.3-red" alt="hmmer">
</p>

---

## 概述
by： jmwang24@outlook.com/wangjm24@mails.tsinghua.edu.cn

**HyBac-PSP** 是一个参考序列驱动的计算预筛选工具，用于在湿实验启动前，从基因组或宏基因组序列中快速锁定高潜力的碱性蛋白酶（subtilisin 家族，MEROPS S8）和碱性脂肪酶（LED I.4 家族）产生菌候选。

该工具是论文 *《基于表型与系统发育分析的加酶洗衣粉碱性水解酶产生菌定向筛选研究方案设计》* 中计算预筛选架构的完整工程实现，旨在为传统纯表型筛选流程提供分子层面的优先级引导。

---

## 核心功能

| 模块 | 功能 |
|------|------|
| **Profile HMM 同源搜索** | 基于 `alk_subtilisin.hmm` 和 `alk_lipase_I4.hmm`，利用 HMMER3 进行高灵敏度家族归属识别 |
| **碱性适应性 PSSM 打分** | 通过位置特异性打分矩阵捕捉催化三联体附近及表面环区的碱性特征信号（Arg/Lys 富集） |
| **双维度综合评分** | `CScore = α·H + (1−α)·B`，融合序列同源性与碱性适应性两个正交维度 |
| **三级优先级判定** | 高/中/低置信度分类，直接输出湿实验验证优先清单 |

---

## 算法设计

### 碱性适应性得分 B

对参考序列多序列比对的每个位点 *i* 和氨基酸 *a*，构建对数优势 PSSM：

$$S_i(a) = \ln\left(\frac{n_i(a) + p}{N_i + 20p}\right) - \ln f_0(a)$$

筛选满足以下条件的核心位点集 *C*：
1. 碱性集与中性对照集氨基酸分布差异显著（χ² 检验，*p* < 0.01）
2. 溶剂可及表面积 > 30%
3. 位于催化三联体 10 Å 范围内或已知影响 pH 活性的表面环区

$$B(x) = \frac{1}{|C|} \sum_{i \in C} S_i(x_i)$$

### 综合评分

$$CScore = \alpha \cdot H + (1 - \alpha) \cdot B$$

默认 *α* = 0.6，高置信度阈值 *τ* = 0.7。


## 项目结构
```
HyBac-PSP/
├── config/default.yaml           # 参数配置
├── data/
│   ├── reference/                # 参考序列集（AlkSub/AlkLipI4 + 中性对照）
│   ├── alignment/                # MAFFT 多序列比对
│   ├── pssm/                     # PSSM 打分矩阵
│   ├── hmm/                      # Profile HMM（HMMER3）
│   └── metadata/                 # 序列来源与文献溯源
├── src/
│   ├── api.py                    # 顶层调用接口
│   ├── hmm_search.py             # HMMER3 封装与解析
│   ├── pssm_scorer.py            # PSSM 打分引擎
│   ├── scoring.py                # 综合评分与优先级判定
│   └── utils.py                  # 序列读写与工具函数
├── scripts/
│   ├── build_reference.py        # 构建参考序列集
│   ├── build_pssm.py             # 构建 PSSM 矩阵
│   ├── build_hmm.py              # 构建 Profile HMM
│   └── run_pipeline.py           # 一键运行
├── tests/
├── docs/
│   ├── methodology.md            # 方法学详细说明
│   └── example_usage.md          # 使用示例
├── requirements.txt
└── setup.py
```


## 依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | ≥ 3.8 | 运行环境 |
| [HMMER](http://hmmer.org/) | 3.3+ | Profile HMM 搜索 |
| [MAFFT](https://mafft.cbrc.jp/alignment/software/) | 7+ | 多序列比对 |
| [CD-HIT](https://github.com/weizhongli/cdhit) | 4.8+ | 序列去冗余 |
| Biopython | ≥ 1.79 | 序列解析 |
| NumPy / Pandas | — | 数值计算与数据输出 |

---

## 安装

```bash
git clone https://github.com/VergilVolk/HyBac-PSP.git
cd HyBac-PSP
pip install -r requirements.txt
```

确保 `hmmsearch`、`mafft`、`cd-hit` 已安装并加入系统 PATH。


## 快速开始

### 1. 构建参考数据库

```bash
python scripts/build_reference.py    # 整理参考序列集
python scripts/build_pssm.py         # 生成 PSSM 矩阵
python scripts/build_hmm.py          # 构建并校准 profile HMM
```

### 2. 运行预筛选

```bash
python src/api.py input_proteins.fasta -o results.csv
```

### 3. 输出解读

| 列名 | 说明 |
|------|------|
| `seq_id` | 输入序列标识符 |
| `H_score` | 归一化序列同源性得分 [0,1] |
| `B_score` | 碱性适应性得分 |
| `CScore` | 综合优先级评分 |
| `priority` | 置信度等级（high/medium/low） |

---

## 适用场景
- 加酶洗涤剂中产碱性酶工业菌株的反向分离与溯源
- 宏基因组数据中碱性水解酶基因的挖掘与宿主推断
- 环境样品中新型碱性蛋白酶/脂肪酶产生菌的定向筛选

---

## 许可证
MIT License. 详见 [LICENSE](LICENSE)。
```
