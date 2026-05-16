"""Tests for infer_role_key_for_device + role-key migration.

Covers:
- NVR family (UNVR / UNVR-Pro / ENVR) routes to the new "NVR" role key.
- Gateways, APs, switches still resolve correctly after dropping the ROUTER branch.
- Legacy ROUTER entries in stored settings collapse into GATEWAY.
- The "Security Appliance" default value is silently refreshed to "Cloud Gateways".
- User-customized GATEWAY values are preserved.
- NVR is seeded on installs that predate this release; never overwritten.
"""
from netbox_unifi.services.sync_engine import infer_role_key_for_device
from netbox_unifi.services._role_migration import DEFAULT_ROLES, migrate_role_keys as _migrate_role_keys


class TestInferRoleKey:
    def test_unvr_pro_is_nvr(self):
        assert infer_role_key_for_device({"model": "UNVR-Pro"}) == "NVR"

    def test_unvr_is_nvr(self):
        assert infer_role_key_for_device({"model": "UNVR"}) == "NVR"

    def test_envr_is_nvr(self):
        assert infer_role_key_for_device({"model": "ENVR"}) == "NVR"

    def test_nvr_detected_via_model_name_text(self):
        device = {"model": "ZZZ", "model_name": "UniFi Protect Network Video Recorder Pro"}
        assert infer_role_key_for_device(device) == "NVR"

    def test_udm_pro_is_gateway(self):
        assert infer_role_key_for_device({"model": "UDMPRO"}) == "GATEWAY"

    def test_legacy_router_model_collapses_into_gateway(self):
        assert infer_role_key_for_device({"model": "ER-X-ROUTER"}) == "GATEWAY"

    def test_routing_feature_is_gateway(self):
        assert infer_role_key_for_device({"model": "MYSTERY", "features": ["routing"]}) == "GATEWAY"

    def test_access_point_is_wireless(self):
        assert infer_role_key_for_device({"model": "U7LT", "is_access_point": True}) == "WIRELESS"

    def test_switch_is_lan(self):
        assert infer_role_key_for_device({"model": "US48PRO", "features": ["switching"]}) == "LAN"

    def test_unknown_falls_through(self):
        assert infer_role_key_for_device({"model": "MYSTERY-9000"}) == "UNKNOWN"


class TestMigrateRoleKeys:
    def test_router_key_collapses_into_gateway(self):
        migrated, changed = _migrate_role_keys({
            "WIRELESS": "Wireless AP",
            "ROUTER": "Router",
            "LAN": "Switch",
            "GATEWAY": "Cloud Gateways",
            "UNKNOWN": "Network Device",
        })
        assert changed is True
        assert "ROUTER" not in migrated
        # Canonical (GATEWAY) wins when both an alias source and target are present.
        assert migrated["GATEWAY"] == "Cloud Gateways"

    def test_router_key_alone_promotes_value_to_gateway(self):
        migrated, _ = _migrate_role_keys({"ROUTER": "Edge Router"})
        assert migrated["GATEWAY"] == "Edge Router"
        assert "ROUTER" not in migrated

    def test_stale_security_appliance_default_renames_to_cloud_gateways(self):
        migrated, changed = _migrate_role_keys({
            "WIRELESS": "Wireless AP",
            "GATEWAY": "Security Appliance",
            "UNKNOWN": "Network Device",
        })
        assert changed is True
        assert migrated["GATEWAY"] == "Cloud Gateways"

    def test_customized_gateway_value_is_preserved(self):
        migrated, _ = _migrate_role_keys({
            "GATEWAY": "My Custom Firewall",
        })
        assert migrated["GATEWAY"] == "My Custom Firewall"

    def test_nvr_is_seeded_when_missing(self):
        migrated, changed = _migrate_role_keys({
            "WIRELESS": "Wireless AP",
            "LAN": "Switch",
            "GATEWAY": "Cloud Gateways",
            "UNKNOWN": "Network Device",
        })
        assert changed is True
        assert migrated["NVR"] == "Camera Security"

    def test_existing_nvr_value_is_preserved(self):
        migrated, _ = _migrate_role_keys({"NVR": "Video Recorders"})
        assert migrated["NVR"] == "Video Recorders"

    def test_idempotent_on_already_migrated_dict(self):
        first, _ = _migrate_role_keys(dict(DEFAULT_ROLES))
        second, changed = _migrate_role_keys(first)
        assert changed is False
        assert second == first
