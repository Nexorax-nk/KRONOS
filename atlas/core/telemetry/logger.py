# atlas/core/telemetry/logger.py
import logging
import re

logger = logging.getLogger("atlas_telemetry")

def secure_system_log(raw_msg: str, **kwargs):
    # Enforces KRONOS-MEMORY-004: Sanitize PII before logging in plaintext log outputs
    sensitive_pattern = re.compile(r"(password|ssn|token|card_number)\s*=\s*\S+", re.IGNORECASE)
    sanitized_msg = sensitive_pattern.sub(r"\1=[REDACTED]", raw_msg)
    logger.info(sanitized_msg, **kwargs)
