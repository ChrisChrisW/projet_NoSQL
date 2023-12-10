from neo4j import GraphDatabase
import os

# Neo4j configuration
class Neo4jDB:
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_user = os.getenv('NEO4J_USER')
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    if not neo4j_uri or not neo4j_user or not neo4j_password:
        raise ValueError("NEO4J_URI, NEO4J_USER, or NEO4J_PASSWORD environment variables are not set.")
    
    def __init__(self):
        self.driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))

    def close(self):
        self.driver.close()

    def create_item(self, field1, field2):
        with self.driver.session() as session:
            session.write_transaction(self._create_item, field1, field2)

    def get_items(self):
        with self.driver.session() as session:
            try:
                return session.read_transaction(self._get_items)
            except Exception as e:
                print(f"Error retrieving Neo4j data: {e}")
                return []
            
    def get_item_by_id(self, item_id):
        with self.driver.session() as session:
            return session.read_transaction(self._get_item_by_id, item_id)

    def edit_item(self, item_id, new_field1, new_field2):
        with self.driver.session() as session:
            session.write_transaction(self._edit_item, item_id, new_field1, new_field2)

    def delete_item(self, item_id):
        with self.driver.session() as session:
            session.write_transaction(self._delete_item, item_id)

    def delete_items(self):
        with self.driver.session() as session:
            try:
                return session.write_transaction(self._delete_items)
            except Exception as e:
                print(f"Error deleting Neo4j data: {e}")
                return []
            
    def _create_item(self, tx, field1, field2):
        tx.run("CREATE (item:Item {field1: $field1, field2: $field2})", field1=field1, field2=field2)
    
    def _get_items(self, tx):
        result = tx.run("MATCH (item:Item) RETURN ID(item) AS id, item.field1 AS field1, item.field2 AS field2")
        return [record for record in result]

    def _get_item_by_id(self, tx, item_id):
        result = tx.run(f"MATCH (item:Item) WHERE ID(item) = {item_id} RETURN ID(item) AS id, item.field1 AS field1, item.field2 AS field2")
        return result.single()
            
    def _edit_item(self, tx, item_id, new_field1, new_field2):
        tx.run(f"MATCH (item:Item) WHERE ID(item) = {item_id} SET item.field1 = '{new_field1}', item.field2 = '{new_field2}'")
    
    def _delete_item(self, tx, item_id):
        tx.run(f"MATCH (item:Item) WHERE ID(item) = {item_id} DELETE item")
    
    def _delete_items(self, tx):
        tx.run(f"MATCH (item:Item) DETACH DELETE item")



