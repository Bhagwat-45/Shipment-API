import sqlite3
from typing import Any

from schema.shipment_schema import ShipmentCreate, ShipmentUpdate

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sqlite3.db",check_same_thread=False)

        self.cur = self.conn.cursor()

        self.create_table()

    def create_table(self):
        create_query = """
            CREATE TABLE IF NOT EXISTS shipment
                ( id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
                )
        """
        self.cur.execute(create_query)

    def create_shipment(self,shipment: ShipmentCreate)->int:
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()

        if result[0] is None:
            new_id = 12701
        else:
            new_id = result[0] + 1

        insert_query = """
        INSERT INTO shipment
        VALUES (:id,:content,:weight,:status);
        """

        self.cur.execute(insert_query,
                         {
                             "id" : new_id,
                             **shipment.model_dump(),
                             "status" : "placed"
                         })
        
        self.conn.commit()

        return new_id

    def get_shipment(self,id:int)-> dict[str,Any] | None:
        select_query = """
        SELECT * FROM shipment WHERE id = :id
        """

        self.cur.execute(select_query,{"id":id})
        row = self.cur.fetchone()


        return {
            "id" : row[0],
            "content" : row[1],
            "weight" : row[2],
            "status" : row[3]
        } if row else None
    
    def update_shipment(self,id:int,shipment: ShipmentUpdate) -> dict[str,Any]:
        update_query = """
        UPDATE shipment SET status = :status
        WHERE id = :id;
        """
        self.cur.execute(update_query,{
            "status" : shipment.status, "id" : id
        })
        self.conn.commit()

        return self.get_shipment(id)
    
    def delete(self,id:int):
        delete_query = """
        DELETE FROM shipment
        WHERE id = :id
        """

        self.cur.execute(delete_query,{"id":id})
        self.conn.commit()

    def close(self):
        self.conn.close()




