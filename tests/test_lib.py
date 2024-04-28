from compose_pydantic import ComposeSpecificationFactory, ComposeSpecification, FileSpecStrategy, TextSpecStrategy


def test_compose_specification_factory():
    compose_strategy = ComposeSpecificationFactory(strategy=TextSpecStrategy())
    compose_spec = """
version: "3.9"
services:
  db:
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    depends_on:
      - db
    """
    assert isinstance(compose_strategy(compose_spec), ComposeSpecification)

    compose_strategy = ComposeSpecificationFactory(strategy=FileSpecStrategy())
    assert isinstance(compose_strategy('./tests/compose/docker-compose.yml', ['./tests/compose/docker-compose.override.yml']), ComposeSpecification)
