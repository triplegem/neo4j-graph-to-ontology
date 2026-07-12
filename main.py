from ontology_toolkit.connection import get_driver
from ontology_toolkit.discover_schema import discover_schema
from ontology_toolkit.printer import print_schema


def main():

    driver = get_driver()

    try:

        driver.verify_connectivity()

        print("Connected to Neo4j!")

        schema = discover_schema(driver)

        print_schema(schema)

    finally:

        driver.close()


if __name__ == "__main__":
    main()