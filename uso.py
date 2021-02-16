from listas_ligadas import Lista


nomes = Lista(['Fulano', 'Beltrano', 'Sicrano'])

print(nomes)

for i, e in enumerate(nomes):
    print('i - {} | Nome: {}'.format(i, e))