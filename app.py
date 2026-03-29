"""PLANWISE — AI Structural Intelligence System (Entry Point)"""

import sys
from pipeline import run_pipeline


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(input_path=input_path)


if __name__ == "__main__":
    main()
