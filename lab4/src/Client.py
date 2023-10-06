import xmlrpc.client

proxy = xmlrpc.client.ServerProxy('http://localhost:8888')
proxy.register("admin", "admin")
proxy.create("topic1", "description1", "admin")
proxy.subject()
