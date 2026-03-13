import os
import pytest
from core.cli import parse_args

def test_cli_parsing():
    # Test with dummy args
    import sys
    sys.argv = ["snaprecon.py", "-d", "example.com"]
    args = parse_args()
    assert args.domain == "example.com"
    assert args.all is False

def test_wordlist_exists():
    assert os.path.exists("wordlists/default.txt")
