# src/utils/logger.py
import logging
import re

logger = logging.getLogger("kronos_app")

def secure_log(message: str, **kwargs):
    # Enforces KRONOS-MEMORY-004: Sanitize PII before logging
    pii_pattern = re.compile(r"(password|ssn|token|card_number)\s*=\s*\S+", re.IGNORECASE)
    sanitized = pii_pattern.sub(r"\1=[REDACTED]", message)
    logger.info(sanitized, **kwargs)
