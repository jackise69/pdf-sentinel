# systemd Service

Run PDF Sentinel as a systemd user service for 24/7 operation on Linux.

## Installation

```bash
pdf-sentinel install --input /path/to/input --output /path/to/output
```

This creates and enables a systemd user service at:
```
~/.config/systemd/user/pdf-sentinel.service
```

## Service Management

### Check Status

```bash
systemctl --user status pdf-sentinel
```

### Start Service

```bash
systemctl --user start pdf-sentinel
```

### Stop Service

```bash
systemctl --user stop pdf-sentinel
```

### Restart Service

```bash
systemctl --user restart pdf-sentinel
```

### Enable on Boot

```bash
systemctl --user enable pdf-sentinel
```

### Disable on Boot

```bash
systemctl --user disable pdf-sentinel
```

## View Logs

### Real-time Logs

```bash
journalctl --user -u pdf-sentinel -f
```

### Recent Logs

```bash
journalctl --user -u pdf-sentinel -n 100
```

### Logs Since Boot

```bash
journalctl --user -u pdf-sentinel -b
```

## Service File

Location: `~/.config/systemd/user/pdf-sentinel.service`

```ini
[Unit]
Description=PDF Sentinel - PDF to Markdown Conversion Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/pdf-sentinel start --input /path/to/input --output /path/to/output
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

## Troubleshooting

### Service Won't Start

Check service status:
```bash
systemctl --user status pdf-sentinel
```

View error logs:
```bash
journalctl --user -u pdf-sentinel -n 50
```

### Service Stops Unexpectedly

Enable lingering (keeps user services running when logged out):
```bash
loginctl enable-linger $USER
```

### Permission Issues

Ensure directories exist and are writable:
```bash
mkdir -p /path/to/input /path/to/output
chmod 755 /path/to/input /path/to/output
```

## Advanced Configuration

### Custom Environment Variables

Edit service file manually:
```bash
systemctl --user edit pdf-sentinel
```

Add environment variables:
```ini
[Service]
Environment="PDF_SENTINEL_ENGINE=markitdown"
Environment="PDF_SENTINEL_MAX_RETRIES=5"
Environment="PDF_SENTINEL_LOG_LEVEL=DEBUG"
```

Reload and restart:
```bash
systemctl --user daemon-reload
systemctl --user restart pdf-sentinel
```

### Resource Limits

Limit CPU and memory usage:
```bash
systemctl --user edit pdf-sentinel
```

```ini
[Service]
CPUQuota=50%
MemoryLimit=500M
```

## Next Steps

- **[Troubleshooting](../troubleshooting.md)** - Common issues and solutions
- **[CLI Usage](cli-usage.md)** - Command-line reference
