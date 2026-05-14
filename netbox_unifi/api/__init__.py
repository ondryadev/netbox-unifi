"""
JSON API endpoints for netbox_unifi.

Mounted at /plugins/unifi-sync/api/ via urls.py.

Endpoints:
  GET  api/status/                      — plugin status and latest run summary
  POST api/controllers/<pk>/test/       — test a controller connection (returns JSON)
"""
