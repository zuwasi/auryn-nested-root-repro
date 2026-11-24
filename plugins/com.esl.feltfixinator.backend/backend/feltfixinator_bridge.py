import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

import llm_client
import violation_loader


class Bridge:
    def _ensure_llm_client(self):
        return llm_client.LLMClient()

    def _ensure_violation_loader(self):
        return violation_loader
