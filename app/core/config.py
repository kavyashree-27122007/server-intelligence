"""
Core configuration loader for Support Intelligence.
Reads from config/config.yaml and .env environment variables.
"""
import os
from pathlib import Path
from typing import List, Optional
import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if not (PROJECT_ROOT / "data").exists():
    if Path("data").exists():
        PROJECT_ROOT = Path(".").resolve()
    elif (Path(__file__).resolve().parent.parent / "data").exists():
        PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

DEFAULT_CONFIG = {
    "brand": "SpotifyCares",
    "brand_twitter_handle": "@SpotifyCares",
    "data": {
        "raw_path": "data/raw/twcs.csv",
        "processed_path": "data/processed",
        "sample_path": "data/processed/sample.csv",
        "index_path": "data/index",
        "golden_set_path": "data/golden_set.csv",
        "sample_size": 8000,
        "random_seed": 42,
        "train_ratio": 0.8,
        "dev_ratio": 0.1,
        "test_ratio": 0.1,
    },
    "classification": {
        "num_intents": 9,
        "min_examples_per_intent": 20,
        "confidence_threshold": 0.35,
    },
    "retrieval": {
        "embedding_model": "all-MiniLM-L6-v2",
        "top_k": 5,
        "similarity_threshold": 0.35,
        "index_type": "hybrid",
    },
    "llm": {
        "provider": "evidence_synthesis",
        "model": "evidence-synthesizer",
        "temperature": 0.2,
        "max_tokens": 200,
        "timeout": 30,
    },
    "escalation": {
        "low_confidence_threshold": 0.45,
        "low_similarity_threshold": 0.35,
        "max_auto_handle_confidence": 0.85,
    },
    "evaluation": {
        "golden_set_path": "data/golden_set.csv",
        "results_dir": "evaluation",
        "judge_model": "gemini-1.5-flash",
    },
    "api": {
        "host": "0.0.0.0",
        "port": 8000,
        "cors_origins": ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:8000"],
        "max_message_length": 5000,
    }
}

def _load_yaml() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    return loaded
        except Exception:
            pass
    return DEFAULT_CONFIG

_cfg = _load_yaml()


class DataConfig:
    raw_path: str = _cfg["data"]["raw_path"]
    processed_path: str = _cfg["data"]["processed_path"]
    sample_path: str = _cfg["data"]["sample_path"]
    index_path: str = _cfg["data"]["index_path"]
    golden_set_path: str = _cfg["data"]["golden_set_path"]
    sample_size: int = int(os.getenv("SAMPLE_SIZE", _cfg["data"]["sample_size"]))
    random_seed: int = int(os.getenv("RANDOM_SEED", _cfg["data"]["random_seed"]))
    train_ratio: float = _cfg["data"]["train_ratio"]
    dev_ratio: float = _cfg["data"]["dev_ratio"]
    test_ratio: float = _cfg["data"]["test_ratio"]


class ClassificationConfig:
    num_intents: int = _cfg["classification"]["num_intents"]
    min_examples_per_intent: int = _cfg["classification"]["min_examples_per_intent"]
    confidence_threshold: float = _cfg["classification"]["confidence_threshold"]


class RetrievalConfig:
    embedding_model: str = os.getenv("EMBEDDING_MODEL", _cfg["retrieval"]["embedding_model"])
    top_k: int = _cfg["retrieval"]["top_k"]
    similarity_threshold: float = _cfg["retrieval"]["similarity_threshold"]
    index_type: str = _cfg["retrieval"]["index_type"]


class LLMConfig:
    provider: str = os.getenv("LLM_PROVIDER", _cfg["llm"]["provider"])
    model: str = os.getenv("LLM_MODEL", _cfg["llm"]["model"])
    temperature: float = _cfg["llm"]["temperature"]
    max_tokens: int = _cfg["llm"]["max_tokens"]
    timeout: int = _cfg["llm"]["timeout"]
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")


class EscalationConfig:
    low_confidence_threshold: float = _cfg["escalation"]["low_confidence_threshold"]
    low_similarity_threshold: float = _cfg["escalation"]["low_similarity_threshold"]
    max_auto_handle_confidence: float = _cfg["escalation"]["max_auto_handle_confidence"]


class EvaluationConfig:
    golden_set_path: str = _cfg["evaluation"]["golden_set_path"]
    results_dir: str = _cfg["evaluation"]["results_dir"]
    judge_model: str = os.getenv("JUDGE_MODEL", _cfg["evaluation"]["judge_model"])


class APIConfig:
    host: str = os.getenv("API_HOST", _cfg["api"]["host"])
    port: int = int(os.getenv("API_PORT", _cfg["api"]["port"]))
    cors_origins: List[str] = _cfg["api"]["cors_origins"]
    max_message_length: int = _cfg["api"]["max_message_length"]


class Settings:
    brand: str = os.getenv("BRAND", _cfg["brand"])
    brand_twitter_handle: str = os.getenv("BRAND_HANDLE", _cfg["brand_twitter_handle"])
    project_root: Path = PROJECT_ROOT
    data = DataConfig()
    classification = ClassificationConfig()
    retrieval = RetrievalConfig()
    llm = LLMConfig()
    escalation = EscalationConfig()
    evaluation = EvaluationConfig()
    api = APIConfig()
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
