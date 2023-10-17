import xmlrpc.client

class Client:
    def __init__(self) -> None:
        self.proxy = xmlrpc.client.ServerProxy("http://localhost:8888")
        
    def register(self, username, password):
        res = self.proxy.register(username, password)
        if res:
            print('Register successfully')
            return True
        else:
            print('Register failed')
        return False
        
    def create(self, topic_name, description, founder_name):
        res = self.proxy.create(topic_name, description, founder_name)
        if res:
            print('Create topic successfully')
            return True
        else:
            print('Create topic failed')
        return False

    def subject(self):
        res = self.proxy.subject()
        print(res)
        return res
        
    def reply(self, topic_name, username, content):
        res = self.proxy.reply(topic_name, username, content)
        if res:
            print('Reply successfully')
            return True
        else:
            print('Reply failed')
        return False

    def discussion(self, topic_name):
        res = self.proxy.discussion(topic_name)
        print(res)
        return res

    def delete(self, topic_name):
        res = self.proxy.delete(topic_name)
        if res:
            print('Delete successfully')
            return True
        else:
            print('Delete failed')
        return False

if __name__ == "__main__":
    client = Client()
    client.register('user1', '123')
    client.create('topic1', 'description1', 'user1')
    client.subject()
    client.reply('topic1', 'user2', 'content2')
    client.discussion('topic1')
    client.delete('topic1')