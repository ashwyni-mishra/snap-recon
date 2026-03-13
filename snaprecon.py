"""Main entry point for the Snap-Recon reconnaissance framework."""

import sys
from core.banner import show_banner
from core.cli import parse_args
from core.engine import ReconEngine
from core.logger import Logger
from core.help_module import show_detailed_help


def main() -> None:
    """Initialize and run the Snap-Recon engine based on CLI arguments."""
    args = parse_args()

    # Check for help first
    if args.help or args.h:
        show_banner()
        show_detailed_help()
        sys.exit(0)

    if not args.domain:
        show_banner()
        Logger.error("Missing required argument: -d / --domain. Use --help for usage details.")
        sys.exit(1)

    show_banner()
    Logger.info("Initialization complete")

    engine = ReconEngine(args)

    try:
        engine.run_all()
    except KeyboardInterrupt:
        Logger.warning("Execution interrupted by user")
    except Exception as e:
        Logger.error(f"Fatal error occurred: {e}")


if __name__ == "__main__":
    main()
