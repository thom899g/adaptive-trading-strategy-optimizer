"""
Configuration management for Adaptive Trading Strategy Optimizer
Centralized configuration with environment variable fallbacks
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

@dataclass
class TradingConfig:
    """Main configuration class with validation"""
    
    # Firebase Configuration
    firebase_credentials_path: str = field(
        default_factory=lambda: os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase_credentials.json")
    )
    firestore_collection: str = field(
        default_factory=lambda: os.getenv("FIRESTORE_COLLECTION", "trading_strategies")
    )
    realtime_db_url: str = field(
        default_factory=lambda: os.getenv("FIREBASE_REALTIME_URL", "")
    )
    
    # Trading Configuration
    default_exchange: str = field(
        default_factory=lambda: os.getenv("DEFAULT_EXCHANGE", "binance")
    )
    supported_exchanges: list = field(
        default_factory=lambda: ["binance", "coinbase", "kraken", "bybit"]
    )
    
    # Risk Management
    max_position_size_pct: float = field(
        default_factory=lambda: float(os.getenv("MAX_POSITION_SIZE_PCT", "0.02"))
    )
    max_daily_loss_pct: float = field(
        default_factory=lambda: float(os.getenv("MAX_DAILY_LOSS_PCT", "0.05"))
    )
    stop_loss_pct: float = field(
        default_factory=lambda: float(os.getenv("STOP_LOSS_PCT", "0.02"))
    )
    
    # Data Configuration
    historical_data_days: int = field(
        default_factory=lambda: int(os.getenv("HISTORICAL_DATA_DAYS", "365"))
    )
    timeframe: str = field(
        default_factory=lambda: os.getenv("TIMEFRAME", "1h")
    )
    min_data_points: int = field(
        default_factory=lambda: int(os.getenv("MIN_DATA_POINTS", "1000"))
    )
    
    # ML Configuration
    model_retrain_hours: int = field(
        default_factory=lambda: int(os.getenv("MODEL_RETRAIN_HOURS", "24"))
    )
    prediction_confidence_threshold: float = field(
        default_factory=lambda: float(os.getenv("PREDICTION_CONFIDENCE_THRESHOLD", "0.7"))
    )
    
    # Execution Configuration
    paper_trading: bool = field(
        default_factory=lambda: os.getenv("PAPER_TRADING", "true").lower() == "true"
    )
    max_open_trades: int = field(
        default_factory=lambda: int(os.getenv("MAX_OPEN_TRADES", "5"))
    )
    
    # Logging Configuration
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )
    log_file: str = field(
        default_factory=lambda: os.getenv("LOG_FILE", "trading_optimizer.log")
    )
    
    def validate(self) -> None:
        """Validate configuration parameters"""
        errors = []
        
        # Validate percentages
        if not 0 < self.max_position_size_pct <= 1:
            errors.append(f"max_position_size_pct must be between 0 and 1, got {self.max_position_size_pct}")
        
        if not 0 < self.stop_loss_pct <= 1:
            errors.append(f"stop_loss_pct must be between 0 and 1, got {self.stop_loss_pct}")