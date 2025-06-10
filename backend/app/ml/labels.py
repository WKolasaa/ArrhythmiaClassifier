from .model import CLASS_MAP

def label_to_int(label: str) -> int:
    return CLASS_MAP[label]

def int_to_label(index: int) -> str:
    inverse = {v: k for k, v in CLASS_MAP.items()}
    return inverse[index]
