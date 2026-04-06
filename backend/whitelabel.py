"""
White-Label Configuration -- B2B clinic customization.

Each tenant can customize:
- Brand name, logo URL
- Primary/accent colors
- Contact info
- Custom disclaimer text
"""

import json
from pathlib import Path

WHITELABEL_PATH = Path(__file__).parent / "whitelabel_config.json"

DEFAULT_CONFIG = {
    "brand_name": "MedDiagnose AI",
    "tagline": "Multi-agent clinical analysis",
    "logo_url": None,
    "primary_color": "#3b82f6",
    "accent_color": "#8b5cf6",
    "contact_email": "",
    "contact_phone": "",
    "disclaimer": "This AI-generated assessment is for informational purposes only.",
    "powered_by": True,
}


def get_whitelabel_config() -> dict:
    """Load white-label config from disk, falling back to defaults."""
    if WHITELABEL_PATH.exists():
        try:
            stored = json.loads(WHITELABEL_PATH.read_text())
            # Merge with defaults so new keys are always present
            merged = {**DEFAULT_CONFIG, **stored}
            return merged
        except (json.JSONDecodeError, IOError):
            pass
    return dict(DEFAULT_CONFIG)


def update_whitelabel_config(updates: dict) -> dict:
    """Merge updates into current config and persist."""
    current = get_whitelabel_config()
    # Only allow known keys
    for key in DEFAULT_CONFIG:
        if key in updates:
            current[key] = updates[key]
    WHITELABEL_PATH.write_text(json.dumps(current, indent=2))
    return current
