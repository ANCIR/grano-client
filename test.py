
from granoclient import Grano

client = Grano(api_key='7a8badec6052a81d5')
project = client.get('openinterests')
print project.label

print list(client.projects)

data = {'slug': 'foo', 'label': 'The Foo Project'}
p = client.projects.create(data)
print p
