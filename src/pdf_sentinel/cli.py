"""Command-line interface for PDF Sentinel."""

import sys
import argparse
import logging
from pathlib import Path

from pdf_sentinel import PDFSentinel, Config, __version__
from pdf_sentinel.config import ConversionEngine
from pdf_sentinel.converters import PyMuPDFConverter, MarkItDownConverter, PDFPlumberConverter

logger = logging.getLogger(__name__)


def cmd_start(args):
    """Start the PDF watcher service."""
    config = Config(
        input_dir=args.input,
        output_dir=args.output,
        engine=args.engine,
        max_retries=args.retries,
        log_level=args.log_level
    )

    sentinel = PDFSentinel(config)
    sentinel.start(scan_existing=not args.no_scan)


def cmd_convert(args):
    """Convert a single PDF file."""
    pdf_path = Path(args.input)
    output_path = Path(args.output) if args.output else pdf_path.with_suffix('.md')

    if not pdf_path.exists():
        print(f"Error: Input file not found: {pdf_path}")
        sys.exit(1)

    # Get converter
    if args.engine == "pymupdf4llm":
        converter = PyMuPDFConverter()
    elif args.engine == "markitdown":
        converter = MarkItDownConverter()
    elif args.engine == "pdfplumber":
        converter = PDFPlumberConverter()
    else:
        print(f"Error: Unknown engine: {args.engine}")
        sys.exit(1)

    # Convert
    print(f"Converting {pdf_path.name} with {converter.name}...")
    success, error_msg = converter.convert(pdf_path, output_path)

    if success:
        print(f"✓ Successfully converted to {output_path}")
        sys.exit(0)
    else:
        print(f"✗ Conversion failed: {error_msg}")
        sys.exit(1)


def cmd_install(args):
    """Install systemd service (Linux only)."""
    import platform
    import subprocess
    import shutil

    if platform.system() != "Linux":
        print("Error: systemd installation is only supported on Linux")
        sys.exit(1)

    service_template = """[Unit]
Description=PDF Sentinel - Event-Driven PDF to Markdown Conversion
After=default.target

[Service]
Type=simple
WorkingDirectory={working_dir}
ExecStart={python_path} -m pdf_sentinel start --input {input_dir} --output {output_dir}
Restart=on-failure
RestartSec=10

# Environment variables
Environment="PDF_CONVERTER={engine}"

# Logging
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=default.target
"""

    # Get paths
    working_dir = Path.cwd()
    python_path = sys.executable
    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()
    engine = args.engine

    # Create directories
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Service file path
    service_dir = Path.home() / ".config" / "systemd" / "user"
    service_dir.mkdir(parents=True, exist_ok=True)
    service_file = service_dir / "pdf-sentinel.service"

    # Write service file
    service_content = service_template.format(
        working_dir=working_dir,
        python_path=python_path,
        input_dir=input_dir,
        output_dir=output_dir,
        engine=engine
    )

    with open(service_file, 'w') as f:
        f.write(service_content)

    print(f"✓ Service file created: {service_file}")

    # Reload systemd
    try:
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        print("✓ Systemd daemon reloaded")

        # Enable service
        if not args.no_enable:
            subprocess.run(["systemctl", "--user", "enable", "pdf-sentinel.service"], check=True)
            print("✓ Service enabled (will start on login)")

        # Start service
        if not args.no_start:
            subprocess.run(["systemctl", "--user", "start", "pdf-sentinel.service"], check=True)
            print("✓ Service started")

        print("\nService management commands:")
        print("  systemctl --user status pdf-sentinel.service")
        print("  systemctl --user stop pdf-sentinel.service")
        print("  systemctl --user restart pdf-sentinel.service")
        print("  journalctl --user -u pdf-sentinel.service -f")

    except subprocess.CalledProcessError as e:
        print(f"Error managing systemd service: {e}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PDF Sentinel - Event-driven PDF to Markdown conversion",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"PDF Sentinel {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser(
        "start",
        help="Start the PDF watcher service"
    )
    start_parser.add_argument(
        "--input", "-i",
        type=str,
        default="./input",
        help="Input directory for PDFs (default: ./input)"
    )
    start_parser.add_argument(
        "--output", "-o",
        type=str,
        default="./output",
        help="Output directory for markdown files (default: ./output)"
    )
    start_parser.add_argument(
        "--engine", "-e",
        type=str,
        choices=["pymupdf4llm", "markitdown", "pdfplumber"],
        default="pymupdf4llm",
        help="Conversion engine (default: pymupdf4llm)"
    )
    start_parser.add_argument(
        "--retries", "-r",
        type=int,
        default=2,
        help="Maximum retry attempts (default: 2)"
    )
    start_parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    start_parser.add_argument(
        "--no-scan",
        action="store_true",
        help="Don't process existing PDFs on startup"
    )
    start_parser.set_defaults(func=cmd_start)

    # Convert command
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert a single PDF file"
    )
    convert_parser.add_argument(
        "input",
        type=str,
        help="Input PDF file"
    )
    convert_parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output markdown file (default: same name as input with .md extension)"
    )
    convert_parser.add_argument(
        "--engine", "-e",
        type=str,
        choices=["pymupdf4llm", "markitdown", "pdfplumber"],
        default="pymupdf4llm",
        help="Conversion engine (default: pymupdf4llm)"
    )
    convert_parser.set_defaults(func=cmd_convert)

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install systemd service (Linux only)"
    )
    install_parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="Input directory for PDFs"
    )
    install_parser.add_argument(
        "--output", "-o",
        type=str,
        required=True,
        help="Output directory for markdown files"
    )
    install_parser.add_argument(
        "--engine", "-e",
        type=str,
        choices=["pymupdf4llm", "markitdown", "pdfplumber"],
        default="pymupdf4llm",
        help="Conversion engine (default: pymupdf4llm)"
    )
    install_parser.add_argument(
        "--no-enable",
        action="store_true",
        help="Don't enable service auto-start"
    )
    install_parser.add_argument(
        "--no-start",
        action="store_true",
        help="Don't start service immediately"
    )
    install_parser.set_defaults(func=cmd_install)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Execute command
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if args.command == "start" and hasattr(args, 'log_level') and args.log_level == "DEBUG":
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
