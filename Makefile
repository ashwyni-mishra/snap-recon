.PHONY: help install test clean

help:
	@echo "Snap-Recon Makefile"
	@echo "-------------------"
	@echo "setup   - Run setup.sh (venv + alias for Linux/Kali)"
	@echo "install - Install dependencies, the tool, and the man page (System-wide)"
	@echo "test    - Run tests"
	@echo "clean   - Remove build artifacts and temporary files"

setup:
	chmod +x setup.sh
	./setup.sh

install:
	pip install -r requirements.txt
	pip install .
	@if [ -d "/usr/local/share/man/man1" ]; then \
		echo "Installing manual page..."; \
		sudo cp docs/snap-recon.1 /usr/local/share/man/man1/; \
		sudo mandb; \
	elif [ -d "/usr/share/man/man1" ]; then \
		echo "Installing manual page..."; \
		sudo cp docs/snap-recon.1 /usr/share/man/man1/; \
		sudo mandb; \
	else \
		echo "Manual directory not found. Skipping man page installation."; \
	fi

test:
	pytest

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
