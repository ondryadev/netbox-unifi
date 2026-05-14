from os import getenv

# Imported by NetBox runtime configuration.py in netbox-docker.
# Do not edit /opt/netbox/netbox/netbox/configuration.py directly in container.
PLUGINS = ["netbox_unifi"]

PLUGINS_CONFIG = {
    "netbox_unifi": {}
}
