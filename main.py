from discover import main as discover_main
from validate import main as validate_main


def main():

    print("=" * 60)
    print("Semantic Graph Toolkit")
    print("=" * 60)

    print("\nStep 1: Discovering schema...")
    discover_main()

    print("\nStep 2: Validating graph...")
    validate_main()

    print("\nDone.")


if __name__ == "__main__":
    main()