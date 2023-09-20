import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String

Base = declarative_base()


class Cliente(Base):
    # Nome da Tabela.
    __tablename__ = "cliente"

    # Atributos da Tabela
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))

    # Relacionamento entre as tabelas Cliente e conta.
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    # Nome da Tabela.
    __tablename__ = "conta"

    # Atributos da Tabela.
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(Float)

    # Relacionamento entre as tabelas Conta e Cliente.
    cliente = relationship(
        "Cliente", back_populates="conta"
    )

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"


# Conexão com o banco de dados.
engine = create_engine("sqlite://")
# Criação das tabelas no banco.
Base.metadata.create_all(engine)
# Definindo valores para os atributos.
with Session(engine) as session:
    guilherme = Cliente(
        nome='Guilherme',
        cpf='12365478910',
        endereco='Avenida',
        conta=[Conta(tipo='Corrente',
                     agencia='2222',
                     num=11111110,
                     saldo=999.0)]
    )

    miguel = Cliente(
        nome='Miguel',
        cpf='11122233310',
        endereco='Avenida',
        conta=[Conta(tipo='Poupança',
                     agencia='2121',
                     num=22222220,
                     saldo=9.0)]
    )

    pedro = Cliente(
        nome='Pedro',
        cpf='99988877710',
        endereco='Avenida',
        conta=[Conta(tipo='Poupança',
                     agencia='2222',
                     num=44444440,
                     saldo=1000.0)]
    )

    alex = Cliente(
        nome='Alex',
        cpf='77788855530',
        endereco='Avenida',
        conta=[Conta(tipo='Corrente',
                     agencia='1111',
                     num=12121210,
                     saldo=0.0)]
    )

    session.add_all([guilherme, miguel, pedro, alex])

    session.commit()

print("\n=========================================================\n")

# Consultando informações na tabela.
declaracao = select(Cliente).where(Cliente.nome.in_(['Guilherme']))

for cliente in session.scalars(declaracao):
    print(cliente)

declaracao_conta = select(Conta).where(Conta.id.in_([1]))

for conta in session.scalars(declaracao_conta):
    print(conta)

# Ordenando as informações de forma decrescente.
ordem = select(Cliente.nome).order_by(Cliente.nome.desc())
print("\n=========================================================\n")
for ordenado in session.scalars(ordem):
    print(ordenado)

# Ordenando as informações de forma crescente.
ordem = select(Cliente.nome).order_by(Cliente.nome)
print("\n=========================================================\n")
for ordenado in session.scalars(ordem):
    print(ordenado)

# Usando o Join para fazer a junção de colunas de duas tabelas.
dec_join = select(Cliente.nome, Conta.tipo).join_from(Cliente, Conta)
connection = engine.connect()
resultados = connection.execute(dec_join).fetchall()
print("\n=========================================================\n")
for resultado in resultados:
    print(resultado)

# Contando a quantidade de instancias na tabela.
contagem = select(func.count('*')).select_from(Cliente)
for resultado in session.scalars(contagem):
    print(resultado)
