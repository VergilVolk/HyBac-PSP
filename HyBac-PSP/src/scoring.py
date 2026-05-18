def compute_cscore(H, B, alpha=0.6):
    """综合评分"""
    return alpha * H + (1 - alpha) * B

def classify(cscore, high=0.7, medium=0.4):
    if cscore >= high:
        return "high"
    elif cscore >= medium:
        return "medium"
    else:
        return "low"