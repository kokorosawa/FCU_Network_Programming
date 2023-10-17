import xmlrpc.client
import json


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
            print(f'Create topic {topic_name} successfully')
            return True
        else:
            print('Topic alreay exists or create')
        return False

    def subject(self):
        res = self.proxy.subject()
        reslist = json.loads(res)
        for i in reslist:
            print(
                F"Topic name: {i['topic_name']}, Description: {i['description']}, \nFounder name: {i['founder_name']}, Founded time: {i['founded_time']}")
            print('----------------------------------------')
        return res

    def reply(self, topic_name, username, content):
        res = self.proxy.reply(topic_name, username, content)
        if res:
            print('Reply successfully')
            print('your reply: ', content)
            return True
        else:
            print('Reply failed')
        return False

    def discussion(self, topic_name):
        res = self.proxy.discussion(topic_name)
        reslist = json.loads(res)
        reslist = sorted(reslist, key=lambda x: x['id'])
        for i in reslist:
            print(
                F"ID: {i['id']}, Username: {i['username']},\nContent: {i['content']}, \nTime: {i['time']}")
            print('----------------------------------------')
        return res

    def delete(self, topic_name):
        res = self.proxy.delete(topic_name)
        if res:
            print('Delete ' + topic_name + ' successfully')
            return True
        else:
            print('Delete failed')
        return False


if __name__ == "__main__":
    client = Client()
    client.create('topic1', 'description1', 'user1')
    client.reply('topic1', 'user1', 'content1')
    client.reply('topic1', 'user1', 'content1')
    client.delete('topic1')
