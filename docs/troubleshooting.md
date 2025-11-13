# PDF Sentinel - Troubleshooting Guide

## Quick Diagnostic Commands

Before diving into specific issues, run these commands to gather information:

```bash
# Check service status
systemctl --user status pdf-watcher.service

# View recent logs
journalctl --user -u pdf-watcher.service -n 50

# View errors only
journalctl --user -u pdf-watcher.service -p err -n 50

# Check application log
tail -50 /path/to/pdf-conversions/pdf_watcher.log

# List failed conversions
ls -la /path/to/pdf-conversions/input/failed/
cat /path/to/pdf-conversions/input/failed/*.error.txt
```

## Common Issues

### 1. Service Not Running

**Symptoms:**
- `systemctl --user status pdf-watcher.service` shows "inactive (dead)"
- PDFs in input/ folder are not being processed

**Diagnosis:**

```bash
# Check service status
systemctl --user status pdf-watcher.service

# View error logs
journalctl --user -u pdf-watcher.service -p err -n 50
```

**Common Causes:**

#### A. Python Virtual Environment Not Found

**Error message:**
```
python: can't open file '/path/to/venv/bin/python': [Errno 2] No such file or directory
```

**Solution:**
1. Verify virtual environment exists:
   ```bash
   ls -la /path/to/venv/bin/python
   ```

2. If missing, create it:
   ```bash
   python3 -m venv /path/to/venv
   source /path/to/venv/bin/activate
   pip install watchdog markitdown pdfplumber
   ```

3. Update service file with correct path:
   ```bash
   nano ~/.config/systemd/user/pdf-watcher.service
   # Update ExecStart path
   systemctl --user daemon-reload
   systemctl --user restart pdf-watcher.service
   ```

#### B. Missing Python Dependencies

**Error message:**
```
ModuleNotFoundError: No module named 'watchdog'
```

**Solution:**
```bash
source /path/to/venv/bin/activate
pip install watchdog markitdown pdfplumber
systemctl --user restart pdf-watcher.service
```

#### C. Permission Denied

**Error message:**
```
PermissionError: [Errno 13] Permission denied: '/path/to/pdf-conversions'
```

**Solution:**
```bash
# Fix directory permissions
chmod -R u+rwx /path/to/pdf-conversions
systemctl --user restart pdf-watcher.service
```

#### D. Script Not Found

**Error message:**
```
python: can't open file '/path/to/pdf_watcher.py': [Errno 2] No such file or directory
```

**Solution:**
1. Verify script exists:
   ```bash
   ls -la /path/to/pdf-conversions/pdf_watcher.py
   ```

2. If missing, reinstall or copy from skill assets:
   ```bash
   cp /path/to/skill/assets/pdf_watcher_v2.py /path/to/pdf-conversions/pdf_watcher.py
   chmod +x /path/to/pdf-conversions/pdf_watcher.py
   ```

### 2. PDFs Not Being Processed

**Symptoms:**
- Service is running
- PDFs remain in input/ folder
- No markdown files appear in output/

**Diagnosis:**

```bash
# Watch logs in real-time
journalctl --user -u pdf-watcher.service -f

# Check application log
tail -f /path/to/pdf-conversions/pdf_watcher.log

# Verify file is actually PDF
file /path/to/pdf-conversions/input/yourfile.pdf
```

**Common Causes:**

#### A. File Extension Not .pdf

**Problem:** Only files ending in `.pdf` (lowercase) are processed.

**Solution:**
```bash
# Rename file
mv input/document.PDF input/document.pdf
```

#### B. File Still Being Written

**Problem:** File is being copied and not yet complete.

**Solution:** Wait a moment after copying large files. The system waits 0.5s before processing.

#### C. Incorrect Directory

**Problem:** PDF is in wrong directory.

**Solution:**
```bash
# Verify correct input directory from service
systemctl --user cat pdf-watcher.service | grep WorkingDirectory

# Move file to correct location
mv /wrong/path/file.pdf /correct/path/input/file.pdf
```

#### D. File Already Processed

**Problem:** File was already processed and moved.

**Solution:**
```bash
# Check processed directory
ls -la /path/to/pdf-conversions/input/processed/

# Check if markdown exists
ls -la /path/to/pdf-conversions/output/*.md
```

#### E. Service Crashed

**Problem:** Service stopped unexpectedly.

**Solution:**
```bash
# Check service status
systemctl --user status pdf-watcher.service

# View crash logs
journalctl --user -u pdf-watcher.service -n 100

# Restart service
systemctl --user restart pdf-watcher.service
```

### 3. Conversion Failures

**Symptoms:**
- PDFs move to `input/failed/` directory
- `.error.txt` files appear alongside failed PDFs
- Service logs show conversion errors

**Diagnosis:**

```bash
# List failed conversions
ls -la /path/to/pdf-conversions/input/failed/

# Read error logs
cat /path/to/pdf-conversions/input/failed/*.error.txt

# Check recent errors in service
journalctl --user -u pdf-watcher.service -p err -n 20
```

**Common Causes:**

#### A. Corrupted PDF

**Error message:**
```
Error: PDF is damaged or cannot be opened
```

**Solution:**
1. Verify PDF is valid:
   ```bash
   pdfinfo input/failed/yourfile.pdf
   ```

2. Try to repair:
   ```bash
   # Using gs (Ghostscript)
   gs -o repaired.pdf -sDEVICE=pdfwrite damaged.pdf
   ```

3. Try alternative conversion engine:
   - Edit service file
   - Change `PDF_CONVERTER=markitdown` to `PDF_CONVERTER=pdfplumber`
   - Restart service and retry

#### B. Password-Protected PDF

**Error message:**
```
Error: PDF is encrypted
```

**Solution:**
1. Remove password using `qpdf`:
   ```bash
   qpdf --decrypt --password=yourpassword input.pdf output.pdf
   ```

2. Or use `pdftk`:
   ```bash
   pdftk input.pdf input_pw yourpassword output output.pdf
   ```

#### C. Unsupported PDF Format

**Error message:**
```
Error: Unsupported PDF version or features
```

**Solution:**
1. Try converting to PDF/A:
   ```bash
   gs -dPDFA -dBATCH -dNOPAUSE -sOutputFile=output.pdf -sDEVICE=pdfwrite input.pdf
   ```

2. Try different conversion engine (MarkItDown or pdfplumber)

#### D. Out of Memory

**Error message:**
```
MemoryError: Unable to allocate memory
```

**Solution:**
1. Check system memory:
   ```bash
   free -h
   ```

2. For very large PDFs, split them:
   ```bash
   # Using pdftk
   pdftk large.pdf burst
   # Process each page separately
   ```

3. Increase swap space if needed

#### E. Scanned PDF (Image-Only)

**Error message:**
```
Warning: No text extracted (image-only PDF)
```

**Solution:**
1. Use OCR tool:
   ```bash
   # Using ocrmypdf
   ocrmypdf input.pdf output.pdf
   # Then convert the OCR'd PDF
   ```

2. Or switch to a converter with OCR support

### 4. Service Won't Start After Reboot

**Symptoms:**
- Service works when started manually
- Service doesn't start automatically after reboot/logout

**Diagnosis:**

```bash
# Check if service is enabled
systemctl --user is-enabled pdf-watcher.service

# Check linger status
loginctl show-user $USER | grep Linger
```

**Solution:**

```bash
# Enable service
systemctl --user enable pdf-watcher.service

# Enable linger (service survives logout)
loginctl enable-linger $USER

# Verify
systemctl --user status pdf-watcher.service
```

### 5. High Memory Usage

**Symptoms:**
- Service uses more than expected memory (>100MB when idle)
- System performance degrades

**Diagnosis:**

```bash
# Check service memory usage
systemctl --user status pdf-watcher.service | grep Memory

# Watch memory over time
watch -n 2 'systemctl --user status pdf-watcher.service | grep Memory'
```

**Expected Memory Usage:**
- Idle: ~0MB (process sleeps)
- Active (converting): 60-70MB
- After conversion: Should return to ~0MB

**Common Causes:**

#### A. Multiple PDFs Being Processed

**Problem:** Large batch of PDFs being processed simultaneously.

**Solution:** Normal behavior. Memory will decrease after processing completes.

#### B. Memory Leak

**Problem:** Memory increases over time and doesn't release.

**Solution:**
```bash
# Restart service to clear
systemctl --user restart pdf-watcher.service

# If problem persists, check for stuck processes
ps aux | grep pdf_watcher
```

#### C. Very Large PDF

**Problem:** Single PDF is extremely large (>100MB).

**Solution:**
- Split large PDFs into smaller chunks
- Increase system memory
- Process separately with manual conversion

### 6. Slow Conversion Speed

**Symptoms:**
- Conversions take longer than expected
- Multiple seconds per page

**Diagnosis:**

```bash
# Check which engine is being used
grep "Conversion Engine" /path/to/pdf-conversions/pdf_watcher.log

# Check conversion times
grep "conversion complete" /path/to/pdf-conversions/pdf_watcher.log | tail -10
```

**Common Causes:**

#### A. Using pdfplumber Engine

**Problem:** pdfplumber is slower than MarkItDown.

**Solution:**
```bash
# Switch to MarkItDown
nano ~/.config/systemd/user/pdf-watcher.service
# Change: Environment="PDF_CONVERTER=markitdown"
systemctl --user daemon-reload
systemctl --user restart pdf-watcher.service
```

**Expected Speeds:**
- MarkItDown: ~0.06s per page
- pdfplumber: ~0.35s per page

#### B. CPU Throttling

**Problem:** System is throttling CPU due to temperature or power.

**Solution:**
```bash
# Check CPU frequency
cat /proc/cpuinfo | grep MHz

# Monitor during conversion
watch -n 1 'grep MHz /proc/cpuinfo'
```

#### C. I/O Bottleneck

**Problem:** Slow disk I/O.

**Solution:**
- Move installation to faster disk (SSD vs HDD)
- Check disk health: `smartctl -a /dev/sda`

### 7. Logs Not Appearing

**Symptoms:**
- `journalctl` shows no logs
- Application log file is empty or missing

**Diagnosis:**

```bash
# Check if journal is running
systemctl --user status systemd-journald

# Verify log file location
systemctl --user cat pdf-watcher.service | grep WorkingDirectory
```

**Solution:**

```bash
# Check log file permissions
ls -la /path/to/pdf-conversions/pdf_watcher.log

# If missing, touch to create
touch /path/to/pdf-conversions/pdf_watcher.log
chmod 644 /path/to/pdf-conversions/pdf_watcher.log

# Restart service
systemctl --user restart pdf-watcher.service

# Verify logs appear
tail -f /path/to/pdf-conversions/pdf_watcher.log
```

### 8. Wrong Output Format

**Symptoms:**
- Markdown output doesn't match expectations
- Tables not formatted correctly
- Missing content

**Diagnosis:**

```bash
# Check which engine was used
grep "Conversion Engine" output/yourfile.md

# Compare different engines
# Try the same PDF with different engines
```

**Solutions:**

#### A. Poor Table Extraction

**Problem:** Tables are mangled or missing.

**Solution:** Switch to pdfplumber (best table handling):
```bash
# Change to pdfplumber
Environment="PDF_CONVERTER=pdfplumber"
```

#### B. Missing Text Content

**Problem:** Text content is incomplete.

**Solution:** Try MarkItDown:
```bash
Environment="PDF_CONVERTER=markitdown"
```

#### C. Formatting Issues

**Problem:** Markdown formatting is inconsistent.

**Solution:**
- MarkItDown: Best for general use and LLM workflows
- pdfplumber: Best for complex layouts and tables

### 9. Environment-Specific Issues

#### WSL (Windows Subsystem for Linux)

**Common Problems:**
- Path issues with Windows-style paths
- systemd not available in WSL1

**Solutions:**
```bash
# Convert Windows path to WSL
cd /mnt/c/Users/YourName/Documents/
# NOT C:\Users\YourName\Documents\

# WSL2 required for systemd
wsl --set-version Ubuntu 2
```

#### Multiple Users

**Problem:** Service works for one user but not another.

**Solution:**
- Each user needs their own service installation
- Service files are user-specific: `~/.config/systemd/user/`
- Use per-user installation directories

## Performance Optimization

### 1. Choose the Right Engine

**For LLM Integration (Default):**
```bash
Environment="PDF_CONVERTER=markitdown"
```

**For Table Quality:**
```bash
Environment="PDF_CONVERTER=pdfplumber"
```

### 2. Batch Processing

For large batches:
1. Copy all PDFs at once to input/
2. Monitor progress: `watch -n 1 'ls input/ | wc -l'`
3. Check statistics in logs

### 3. System Tuning

```bash
# Increase inotify watches if monitoring many directories
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Debugging Tools

### Enable Debug Logging

Edit `pdf_watcher.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    ...
)
```

### Monitor in Real-Time

```bash
# Watch service status
watch -n 1 'systemctl --user status pdf-watcher.service'

# Monitor log file
tail -f /path/to/pdf-conversions/pdf_watcher.log

# Monitor directory
watch -n 1 'ls -lh input/ output/'
```

### Manual Conversion Test

Test conversion without the service:

```bash
source /path/to/venv/bin/activate
cd /path/to/pdf-conversions
python3 -c "
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert('input/test.pdf')
print(result.text_content[:500])  # First 500 chars
"
```

## Getting Help

If issues persist:

1. **Gather Information:**
   ```bash
   # System info
   uname -a
   python3 --version

   # Service status
   systemctl --user status pdf-watcher.service

   # Recent logs
   journalctl --user -u pdf-watcher.service -n 100 > debug.log

   # Failed files
   ls -la input/failed/
   cat input/failed/*.error.txt
   ```

2. **Check Dependencies:**
   ```bash
   source /path/to/venv/bin/activate
   pip list | grep -E "(watchdog|markitdown|pdfplumber)"
   ```

3. **Test Minimal Case:**
   - Try with a simple, known-good PDF
   - Single page, text-only, no images
   - Verify basic functionality works

## Appendix: Error Message Reference

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `No module named 'watchdog'` | Missing dependency | `pip install watchdog` |
| `PDF is encrypted` | Password-protected | Remove password with qpdf |
| `Permission denied` | Wrong permissions | `chmod -R u+rwx directory/` |
| `File not found` | Wrong path | Verify path in service file |
| `MemoryError` | Insufficient RAM | Split large PDFs |
| `PDF is damaged` | Corrupted file | Repair with Ghostscript |
| `Service failed` | Multiple causes | Check `journalctl` logs |

## Preventive Maintenance

**Weekly:**
- Check disk space: `df -h`
- Review failed conversions: `ls input/failed/`
- Check log file size: `ls -lh pdf_watcher.log`

**Monthly:**
- Review service logs for patterns
- Update dependencies: `pip install --upgrade markitdown pdfplumber`
- Clean old processed files if needed

**As Needed:**
- Rotate log files if growing large
- Archive old processed PDFs
- Update Python packages
