# netbox-unifi Wiki

`netbox-unifi` er et NetBox plugin til UniFi -> NetBox sync.

## Diagrammer

![Overview](https://raw.githubusercontent.com/ondryadev/netbox-unifi/main/docs/assets/netbox-unifi-overview.svg)

```mermaid
flowchart LR
    U["UniFi"] --> P["Plugin Jobs"]
    P --> N["NetBox"]
    UI["Plugin UI"] --> P
```

## Quick links

- [Installation](Installation)
- [Configuration](Configuration)
- [Run Sync](Run-Sync)
- [Release and PyPI](Release-and-PyPI)
- [Troubleshooting](Troubleshooting)

## Source docs in repository

- [README](https://github.com/ondryadev/netbox-unifi/blob/main/README.md)
- [Server install](https://github.com/ondryadev/netbox-unifi/blob/main/docs/server-install.md)
- [Configuration](https://github.com/ondryadev/netbox-unifi/blob/main/docs/configuration.md)
- [Troubleshooting](https://github.com/ondryadev/netbox-unifi/blob/main/docs/troubleshooting.md)
- [Release](https://github.com/ondryadev/netbox-unifi/blob/main/docs/release.md)
