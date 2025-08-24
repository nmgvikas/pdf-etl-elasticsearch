import os
import yaml
from typing import Any, Dict

def load_config(path: str = "config/config.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    cfg["elasticsearch"]["url"] = os.getenv("ES_URL", cfg["elasticsearch"]["url"])
    cfg["elasticsearch"]["index"] = os.getenv("ES_INDEX", cfg["elasticsearch"]["index"])
    cfg["paths"]["input_dir"] = os.getenv("INPUT_DIR", cfg["paths"]["input_dir"])
    return cfg
