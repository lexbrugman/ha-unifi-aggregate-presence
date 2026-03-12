# UniFi simplified device tracking

Simplified tracking for UniFi clients, combining them into a single entity. The approach is blacklisting fixed devices, anything else will be used for presence detection.

## Configuration

This integration uses Home Assistant UI configuration (Config Entries).

1. Go to **Settings → Devices & Services → Add Integration**.
2. Select **UniFi simplified device tracking**.
3. Fill in controller host, credentials, site id, home subnet, fixed hosts, and scan interval.

### Fixed hosts

- Plain values are treated as case-insensitive literal hostnames.
- Regex values can be supplied using the `re:` prefix (for example: `re:^iphone-.*$`).
- Enter one fixed-host rule per line in the multiline field.
