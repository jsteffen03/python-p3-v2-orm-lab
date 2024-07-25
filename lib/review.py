from __init__ import CURSOR, CONN
from department import Department
from employee import Employee

import sqlite3
connection = sqlite3.connect('company.db')
cursor = connection.cursor()


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()
        

    def save(self):
        res = cursor.execute(f'''
        INSERT INTO reviews(year, summary, employee_id)
        VALUES("{self.year}","{self.summary}",{self.employee_id})
        ''')
        connection.commit()
        self.id = cursor.lastrowid
        Review.all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        new_review = cls(year, summary, employee_id)
        new_review.save()
        return new_review
   
    @classmethod
    def instance_from_db(cls, row):
        row

        if row in Review.all:
            return Review.all[row]
        
        if row:
            id, year, summary, employee_id = row
            review = cls(year, summary, employee_id, id=id)
            Review.all[id] = review
            return review
        return None
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        res = cursor.execute(f"SELECT * FROM reviews WHERE id = {id}") 
        data = res.fetchone()
        if data:
            return cls.instance_from_db(data)
        return None

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        cursor.execute('''
        UPDATE reviews
        SET year = ?, summary = ?, employee_id = ?
        WHERE id = ?
        ''', (self.year, self.summary, self.employee_id, self.id))
        connection.commit()
        

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        cursor.execute(f'''
        DELETE FROM reviews
        WHERE id = {self.id}
        ''')
        del Review.all[self.id]
        self.id = None
        connection.commit()

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        res = cursor.execute("SELECT * FROM reviews")
        data = res.fetchall()
        all_reviews = []
        for review in data:
            rev = Review(
                id = review[0],
                year = review[1],
                summary = review[2],
                employee_id = review[3]
            )
            all_reviews.append(rev)
        return all_reviews




