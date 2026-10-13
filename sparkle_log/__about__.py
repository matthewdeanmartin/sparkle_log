"""Metadata for sparkle_log."""

__all__ = [
    "__credits__",
    "__dependencies__",
    "__description__",
    "__keywords__",
    "__readme__",
    "__requires_python__",
    "__status__",
    "__title__",
    "__version__",
]

__title__ = "sparkle-log"
__version__ = "1.0.0"
__description__ = "Write sparkline graphs of CPU and memory usage to your logs."
__credits__ = [{"name": "Matthew Martin", "email": "matthewdeanmartin@gmail.com"}]
__readme__ = "README.md"
__requires_python__ = ">=3.11"
__keywords__ = ["monitoring", "logging"]
__status__ = "5 - Production/Stable"
__dependencies__ = ["psutil", "schedule", "sparklines>=0.5.0", "colorlog>=6.8.0"]
