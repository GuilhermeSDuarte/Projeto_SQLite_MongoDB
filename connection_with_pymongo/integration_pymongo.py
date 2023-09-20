import pprint

import pymongo

# Conexão com o banco de dados.
client = pymongo.MongoClient("Conexão com o banco")
# Criação de uma coleção dentro do banco de dados
db = client.test
collection = db.test_collection
# Persistindo dados, aqui coloquei algumas informações aleatórias.
post = [{
    "author": "Guilherme",
    "text": "learning to program",
    "tags": ["learning", "program", "python"]},
    {
        "author": "Miguel",
        "text": "likes to sleep",
        "tags": ["sleep", "bed", "zzz"]
    },
    {
        "author": "Pedro",
        "text": "Miguel's father",
        "tags": ["dad", "father", "son"]
    },
    {
        "author": "Alex",
        "text": "professional video game player",
        "tags": ["video", "game", "profissional", "player"]
    }]

posts = db.posts
# Inserindo os dados na coleção.
dados = posts.insert_many(post)
# Exibindo os dados dentro de post no qual o author Alex exista.
pprint.pprint(db.posts.find_one({"author": "Alex"}))
print("====================================================================")
# Exibindo todos os docs da coleção de forma ordenada.
for post in posts.find({}).sort("author"):
    print(post)
print("====================================================================")
# Deletando um dado da coleção.
print(posts.delete_one({"author": "Pedro"}))
print("====================================================================")
# Exibindo os docs após excluir aquele no qual havia o author Pedro.
for post in posts.find({}):
    print(post)
print("====================================================================")
# Excluindo a coleção.
db['posts'].drop()
