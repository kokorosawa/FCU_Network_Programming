from xmlrpc.server import SimpleXMLRPCServer
import sqlite3
import os
import time
import json
import pandas as pd


class Server_API:
    def __init__(self):
        self.serverdb_path = os.path.dirname(__file__) + '\server.db'
        self.conn = sqlite3.connect(self.serverdb_path)
        print("open database successfully")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS USER
               (username TEXT PRIMARY KEY NOT NULL,
               password TEXT NOT NULL);''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS TOPIC
               (topic_name TEXT PRIMARY KEY NOT NULL,
               description TEXT NOT NULL,
               founder_name TEXT NOT NULL,
               founded_time TEXT NOT NULL);''')
        self.conn.commit()

    def register(self, username, password):
        self.c.execute("SELECT * FROM USER WHERE username = '%s'" % username)
        if self.c.fetchone():
            print("Username: %s already exists" % (username))
            return False
        self.c.execute("INSERT INTO USER (username, password) VALUES ('%s', '%s')" % (
            username, password))
        self.conn.commit()
        print("Sign up: username = %s, password = %s" % (username, password))
        return True

    def create(self, topic_name, description, founder_name):
        self.c.execute(
            "SELECT * FROM TOPIC WHERE topic_name = '%s'" % topic_name)
        if self.c.fetchone():
            print("Topic: %s already exists" % (topic_name))
            return False
        self.c.execute("INSERT INTO TOPIC (topic_name, description, founder_name, founded_time) VALUES ('%s', '%s', '%s', '%s')" %
                       (topic_name, description, founder_name, time.ctime()))
        print("Create topic: topic_name = %s, description = %s, founder_name = %s, founded_time = %s" %
              (topic_name, description, founder_name, time.ctime()))
        self.conn.commit()
        return True

    def subject(self):
        self.c.execute("SELECT * FROM TOPIC")
        table_rows = self.c.fetchall()
        df = pd.DataFrame(table_rows, columns=[
                          'topic_name', 'description', 'founder_name', 'founded_time'])
        result = json.loads(df.to_json(orient="records"))
        parsed = json.dumps(result, indent=4)
        print(parsed)
        return parsed


if __name__ == '__main__':
    server = SimpleXMLRPCServer(('localhost', 8888))
    server.register_instance(Server_API())
    print('Listen on port  %d' % 8888)
    try:
        print('Use Control-C to exit!')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server exit')
