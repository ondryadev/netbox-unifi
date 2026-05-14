from __future__ import annotations

from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem


items = (
    PluginMenuItem(
        link="plugins:netbox_unifi:dashboard",
        link_text="Sync Dashboard",
        permissions=["netbox_unifi.view_syncrun"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_unifi:dashboard",
                title="Run now",
                icon_class="mdi mdi-play-circle",
                permissions=["netbox_unifi.add_syncrun"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_unifi:controllers",
        link_text="Controllers",
        permissions=["netbox_unifi.view_unificontroller"],
    ),
    PluginMenuItem(
        link="plugins:netbox_unifi:mappings",
        link_text="Site mappings",
        permissions=["netbox_unifi.view_sitemapping"],
    ),
    PluginMenuItem(
        link="plugins:netbox_unifi:settings",
        link_text="Settings",
        permissions=["netbox_unifi.change_globalsyncsettings"],
    ),
    PluginMenuItem(
        link="plugins:netbox_unifi:runs",
        link_text="Run history",
        permissions=["netbox_unifi.view_syncrun"],
    ),
    PluginMenuItem(
        link="plugins:netbox_unifi:audit",
        link_text="Audit log",
        permissions=["netbox_unifi.view_pluginauditevent"],
    ),
)

menu = PluginMenu(
    label="UniFi Sync",
    icon_class="mdi mdi-wifi-sync",
    groups=(
        ("Sync", items),
    ),
)

# Disable default registration under the generic "Plugins" menu.
empty_menu_items = ()
