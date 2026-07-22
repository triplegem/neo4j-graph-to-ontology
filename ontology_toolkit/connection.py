from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable
from dotenv import load_dotenv
import os


load_dotenv()


def get_driver():

    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    missing = [
        name
        for name, value in (
            ("NEO4J_URI", uri),
            ("NEO4J_USERNAME", username),
            ("NEO4J_PASSWORD", password),
        )
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing required environment variable(s): {', '.join(missing)}"
        )

    try:

        driver = GraphDatabase.driver(
            uri,
            auth=(
                username,
                password,
            ),
        )

        driver.verify_connectivity()

        return driver

    except AuthError as exc:
        raise RuntimeError(
            "Neo4j authentication failed. Check your username and password."
        ) from exc

    except ServiceUnavailable as exc:
        raise RuntimeError(
            "Unable to connect to Neo4j. Verify the URI and ensure the database is running."
        ) from exc