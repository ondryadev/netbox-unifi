"""Role-key constants and migration logic.

Pure-Python module — no Django imports — so the rules can be unit-tested without
booting NetBox. Imported by both the orchestrator (runtime) and the test suite.
"""
from __future__ import annotations

DEFAULT_ROLES: dict[str, str] = {
    "WIRELESS": "Wireless AP",
    "LAN": "Switch",
    "GATEWAY": "Cloud Gateways",
    "NVR": "Camera Security",
    "UNKNOWN": "Network Device",
}

# Legacy role keys (from older DB records or env vars) and the canonical key they
# should collapse into. ROUTER was dropped in favor of GATEWAY when role names
# were aligned with UniFi Store categories ("Cloud Gateways").
_ROLE_KEY_ALIASES: dict[str, str] = {
    "SWITCH": "LAN",
    "SECURITY": "GATEWAY",
    "ROUTER": "GATEWAY",
    "OTHER": "UNKNOWN",
    "PHONE": "UNKNOWN",
}

# Stale default *values* that should be silently refreshed when the user hasn't
# customized them. Only rewritten when the stored value exactly matches a prior
# default — user-set names are preserved.
_LEGACY_DEFAULT_VALUES: dict[str, dict[str, str]] = {
    "GATEWAY": {"Security Appliance": "Cloud Gateways"},
}

# Canonical role keys that did not exist in earlier releases and should be seeded
# on existing installs (the user can rename or delete after the fact).
_SEED_KEYS: tuple[str, ...] = ("NVR",)


def migrate_role_keys(roles: dict[str, str]) -> tuple[dict[str, str], bool]:
    """Migrate stored role mappings to the canonical schema.

    Operations, in order:
      1. Rename legacy keys per ``_ROLE_KEY_ALIASES``. Canonical key wins if both
         the alias and its target are present in the same mapping.
      2. Refresh stale default values listed in ``_LEGACY_DEFAULT_VALUES`` —
         only when the stored value matches the old default exactly.
      3. Seed any newly-introduced canonical keys from ``_SEED_KEYS``.

    Returns ``(migrated, changed)``; ``changed`` is True iff any rewrite occurred.
    Idempotent: passing an already-migrated dict back through returns
    ``changed=False``.
    """
    result: dict[str, str] = {}
    changed = False
    # Pass 1: insert canonical keys first so they always win regardless of dict
    # iteration order (e.g. stored ROUTER before GATEWAY must not clobber the
    # canonical GATEWAY value).
    for key, value in roles.items():
        if key not in _ROLE_KEY_ALIASES:
            result[key] = value
    # Pass 2: fold aliased keys into their canonical slot only if still empty.
    for key, value in roles.items():
        if key in _ROLE_KEY_ALIASES:
            canonical = _ROLE_KEY_ALIASES[key]
            changed = True
            if canonical not in result:
                result[canonical] = value

    for key, replacements in _LEGACY_DEFAULT_VALUES.items():
        current = result.get(key)
        if current in replacements:
            result[key] = replacements[current]
            changed = True

    for new_key in _SEED_KEYS:
        if new_key not in result and new_key in DEFAULT_ROLES:
            result[new_key] = DEFAULT_ROLES[new_key]
            changed = True

    return result, changed
