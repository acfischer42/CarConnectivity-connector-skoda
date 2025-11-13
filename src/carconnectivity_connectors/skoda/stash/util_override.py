"""Local logging helpers to avoid noisy INFO messages about unexpected API keys.

This module provides a wrapper around the upstream `log_extra_keys` behaviour but:
- logs at DEBUG level (so unexpected keys don't pollute INFO output)
- removes credentials from the dictionary before logging
- truncates long dictionaries for readability
- can be enabled at INFO by setting env var CARCONNECTIVITY_SHOW_EXTRA_KEYS=1
"""
from __future__ import annotations
from typing import Any, Dict, Optional
import logging
import os
import json

from carconnectivity.util import config_remove_credentials

LOG = logging.getLogger("carconnectivity.connectors.skoda-api-debug")


def _truncate(obj: Any, max_len: int = 300) -> str:
    try:
        s = json.dumps(obj, default=str, ensure_ascii=False)
    except Exception:
        s = str(obj)
    if len(s) > max_len:
        return s[:max_len] + '...'
    return s


def log_extra_keys(log: logging.Logger, where: str, dictionary: Dict[str, Any], allowed_keys: Optional[set[str]] = None) -> None:
    """Log unexpected keys more quietly and safely.

    By default this logs at DEBUG. To restore the previous INFO behaviour set
    the environment variable CARCONNECTIVITY_SHOW_EXTRA_KEYS=1.
    """
    if allowed_keys is None:
        allowed_keys = set()
    extra_keys = set(dictionary.keys()) - allowed_keys
    if not extra_keys:
        return

    show_info = os.getenv('CARCONNECTIVITY_SHOW_EXTRA_KEYS', '0') in ('1', 'true', 'True')
    sanitized = config_remove_credentials(dictionary.copy())
    msg = f"Unexpected keys found in {where}: {extra_keys} Dictionary is {_truncate(sanitized)}"
    if show_info:
        log.info(msg)
    else:
        # default: be quiet and log at DEBUG
        log.debug(msg)
