#Build and run a docker container that uses our calculator and outputs 247/12

#S1 Try to persist the answers in a docker volume

#S2 Look into how tou can create SQL lite db with pyuthon. Try and write a simple table using python


from pathlib import Path 
from datetime import datetime 
import sqlite3

class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.me = 2.45

    def get_sum(self):
        return self.a + self.b

    def me_index(self):
        ans = (self.a + self.b) * self.me
        return ans

    def get_difference(self):
        return self.a - self.b

    def get_product(self):
        return self.a * self.b

    def get_division(self):
        return self.a / self.b

if __name__ == "__main__":

    out = Path("/data/Results.txt")

    db_path = Path("/data/calculator.db")

    conn = sqlite3.connect(db_path)

    firstnum = 247
    secondnum = 12

    myCalc = Calculator(a=firstnum,b=secondnum)

    with out.open("a") as f:
        f.write(f"Result of {firstnum}/{secondnum}: {myCalc.get_division()} \n")
        f.write(f"Result of {firstnum}*{secondnum}: {myCalc.get_product()} \n")
        f.write(f"Result of {firstnum}+{secondnum}: {myCalc.get_sum()} \n")
        f.write(f"Result of {firstnum}-{secondnum}: {myCalc.get_difference()} \n")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Results (
                firstnumber REAL NOT NULL,
                secondnumber REAL NOT NULL,
                operator TEXT NOT NULL,
                result REAL NOT NULL
            )
            """
        )
        cursor.execute("""
            INSERT INTO Results (firstnumber, secondnumber, operator, result) VALUES (?,?,?,?)
        """ , (firstnum,secondnum,"/",myCalc.get_division()))

        inserted_id=cursor.lastrowid
        cursor.execute("SELECT * FROM Results WHERE rowid = ?",(inserted_id,))
        added_row = cursor.fetchone()
        print(f"Row added to database:{added_row}")


    conn.close()