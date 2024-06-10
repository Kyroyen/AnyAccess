from django.core.files.storage import Storage

class FakeStorage(Storage):

    def open(self, name, mode="rb"):
        pass

    def save(self, name, content, max_length=None):
        pass

    def path(self, name):
        pass

    def delete(self, name):
        pass

    def exists(self, name):
        pass
    
    def listdir(self, path):
        pass
    
    def size(self, name):
        pass
    
    def url(self, name):
        pass
    
