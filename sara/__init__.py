"""Sara open-source assistant package."""

from .assistant import SaraAssistant
from .search import duckduckgo_search, summarize_search_results
from .cyber import CyberSecurityTools
from .gui import SaraGUI

try:
    from .web_gui import SaraWebGUI
except ImportError:
    SaraWebGUI = None

from .cli import main


