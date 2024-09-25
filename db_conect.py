from astrapy import DataAPIClient


def conectar_db():
    client = DataAPIClient("AstraCS:BzUDJRLewdPAPjIOLJHycYZg:b3eff1ca9a63255d773fc9a3fc02ba16007f5b27f28a08716190007a2586ebd6")  # Substitua pelo seu token
    db = client.get_database_by_api_endpoint(
        "https://b93999e2-60d2-4873-b357-d65b3c8e1e81-us-east-2.apps.astra.datastax.com"
    )
    return db

def get_collection(collection_name):
    db = conectar_db()
    return db.get_collection(collection_name)

