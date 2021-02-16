#######################################################$
# Lista Simplesmente Ligada                            #
#   - Implementação próxima a lista built-in do Python #
# Prof. Ygor Amaral - UFRPE/UAST                       #
#######################################################$

import collections


class Lista:
    # inicializador/construtor da lista
    def __init__(self, seq=None):
        # atributos privados
        self.__primeiro = None
        self.__último = None
        self.__tamanho = 0
        self.__erro = 'índice fora dos limites da lista'
        self.__iterando = None  # auxiliar para iterar com lazy evaluation

        # se o objeto passado no construtor for iterável...
        # pegar os elementos e jogar dentro da lista...
        if seq is not None and isinstance(seq, collections.Iterable):
            for e in seq:
                self.inserir_fim(e)
        elif seq is not None:  # não é iterável
            raise TypeError('o objeto fornecido não é iterável')

    # classe interna para representar cada elemento (nó)
    class Nó:
        # inicializador/construtor de cada nó
        def __init__(self, conteúdo):
            self.conteúdo = conteúdo
            self.próximo = None

        def __iter__(self):
            return self

    def __next__(self):
        if self.__iterando is None:
            self.__iterando = self.__primeiro  # pegando o primeiro sempre atualizado
        else:
            self.__iterando = self.__iterando.próximo

        if self.__iterando is not None:
            return self.__iterando.conteúdo

        # parando de iterar
        raise StopIteration

    # quantidade de elementos
    def __len__(self):
        return self.__tamanho

    # comparando se duas listas são iguais
    def __eq__(self, other):
        if len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    # os elementos atuais são diferentes, listas não são iguais
                    return False

            # listas iguais
            return True

        # o tamanho da listas são diferentes, listas não são iguais
        return False

    # função auxiliar para operação de fatiamento
    def __inicializar_valores_fatiamento(self, item):
        # inicializando valores do fatiamento (slice)
        start = 0 if item.start is None else item.start
        stop = len(self) if item.stop is None else item.stop
        step = 1 if item.step is None else item.step

        # tratando índices negativos
        if start < 0:
            start += len(self)

            # se depois de tratar, start continuar menor que 0, então ficará 0
            if start < 0:
                start = 0

        # tratando índices negativos
        if stop < 0:
            stop += len(self)

        if step == 0:
            raise ValueError('step do fatiamento não pode ser zero')

        return start, stop, step

    # pegando algum elemento a partir de um índice (ou fatiamento tb)
    def __getitem__(self, item):
        if isinstance(item, slice):
            # montar nova lista a partir do fatiamento
            _lista = Lista()

            # inicializando valores do fatiamento (slice)
            start, stop, step = self.__inicializar_valores_fatiamento(item)

            # construir nova lista fatiada (vai até stop sem pegar stop)
            i = start
            while 0 <= i < stop:
                # parar caso tenha ultrapassado a quantidade de elementos
                if i >= len(self):
                    break

                _lista.inserir_fim(self[i])
                i += step  # caso step seja negativo, i ficará menor que 0 e while parará

            return _lista
        else:
            # sem fatiamento, apenas pegar um elemento a partir do índice fornecido

            # tratando índices negativos
            if item < 0:
                item += len(self)

            # informar erro se tiver fora dos limites da lista
            if item < 0 or item >= len(self):
                raise IndexError(self.__erro)

            i = 0
            atual = self.__primeiro  # começa do início
            while i <= item:
                if atual is None:
                    break

                if i == item:
                    return atual.conteúdo

                atual = atual.próximo

                i += 1

    def __setitem__(self, item, value):
        if isinstance(item, slice):
            raise Exception('não disponível')
        else:
            # sem fatiamento, apenas pegar um elemento e alterá-lo a partir do índice fornecido

            # tratando índices negativos
            if item < 0:
                item += len(self)

            # informar erro se tiver fora dos limites da lista
            if item < 0 or item >= len(self):
                raise IndexError(self.__erro)

            i = 0
            atual = self.__primeiro  # começa do início
            while i <= item:
                if atual is None:
                    break

                if i == item:
                    atual.conteúdo = value
                    break

                atual = atual.próximo

                i += 1

    # apagando algum elemento a partir de um índice (ou fatiamento tb)
    def __delitem__(self, item):
        if isinstance(item, slice):
            # inicializando valores do fatiamento (slice)
            start, stop, step = self.__inicializar_valores_fatiamento(item)

            # apagar elementos a partir de uma fatia (vai até stop sem pegar stop)
            i = start
            while 0 <= i < stop:
                # parar caso tenha ultrapassado a quantidade de elementos
                if i >= len(self):
                    break

                del self[i]
                i += step  # caso step seja negativo, i ficará menor que 0 e while parará

                # decrementos para compensar o elemento que foi apagado
                i -= 1
                stop -= 1
        else:
            # sem fatiamento, apenas apagar um elemento a partir do índice fornecido

            # tratando índices negativos
            if item < 0:
                item += len(self)

            # informar erro se tiver fora dos limites da lista
            if item < 0 or item >= len(self):
                raise IndexError(self.__erro)

            i = 0
            anterior = None
            atual = self.__primeiro  # começa do início
            while i <= item:
                if atual is None:
                    break

                if i == item:
                    if anterior is None:
                        # apagando o primeiro elemento da lista
                        self.__primeiro = atual.próximo
                    elif atual.próximo is None:
                        # apagando o último elemento da lista
                        anterior.próximo = None
                        self.__último = anterior
                    else:
                        # apagando um elemento intermediário da lista
                        anterior.próximo = atual.próximo

                    self.__tamanho -= 1

                    return atual.conteúdo

                anterior = atual
                atual = atual.próximo

                i += 1

        self.__iterando = None  # modificou a lista, iterando deve ser reinicializado

    # retornando a lista em formato de string
    def __str__(self):
        retorno = '>'
        for i, e in enumerate(self):
            retorno += e.__repr__()
            if i < len(self) - 1:
                retorno += ', '
        retorno += '<'

        return retorno

    # representação interna na forma bruta
    def __repr__(self):
        return self.__str__()

    # remover e retornar o elemento removido
    def pop(self, i=-1):
        return self.__delitem__(i)

    # remover o primeiro elemento encontrado
    def remover(self, x):
        atual = self.__primeiro
        i = 0
        while atual is not None:
            if atual.conteúdo == x:
                del self[i]
                return

            atual = atual.próximo
            i += 1

        raise ValueError('impossível remover, o elemento não existe na lista')

    # contar a quantidade de ocorrências do elemento encontrado
    def contar(self, x):
        cont = 0

        atual = self.__primeiro
        while atual is not None:
            if atual.conteúdo == x:
                cont += 1

            atual = atual.próximo

        return cont

    # retornar o índice do elemento encontrado
    def index(self, x):
        atual = self.__primeiro
        i = 0
        while atual is not None:
            if atual.conteúdo == x:
                return i

            atual = atual.próximo
            i += 1

        raise ValueError('impossível encontrar, o elemento não existe na lista')

    # inserir elemento no início da lista
    def inserir_início(self, conteúdo):
        self.inserir(0, conteúdo)

    # inserir elemento no fim da lista
    def inserir_fim(self, conteúdo):
        self.inserir(len(self), conteúdo)

    # inserir elemento em qualquer posição da lista
    def inserir(self, índice, conteúdo):
        novo = self.Nó(conteúdo)

        # tratando índices negativos
        if índice < 0:
            índice += len(self)

        # se primeiro é nulo, lista está vazia
        if self.__primeiro is None:
            # nesse caso...
            # terá apenas um único elemento, ele será o primeiro e o último
            self.__primeiro = novo
            self.__último = novo
        elif índice <= 0:  # inserir no início
            # o que era primeiro, será segundo
            # e assim sucessivamente...
            # o novo irá apontar para o que ERA primeiro
            novo.próximo = self.__primeiro

            # será o primeiro, pois, inserimos no início
            self.__primeiro = novo
        elif índice >= len(self):  # inserir no fim
            # o que era o último irá apontar para o novo
            self.__último.próximo = novo

            # será o último, pois, inserimos no fim
            self.__último = novo
        else:  # inserir entre elementos
            i = 0
            anterior = None
            atual = self.__primeiro  # começa do início
            while i <= índice:
                if atual is None:
                    break

                if i == índice:
                    novo.próximo = anterior.próximo
                    anterior.próximo = novo
                    break

                anterior = atual
                atual = atual.próximo

                i += 1

        self.__iterando = None  # modificou a lista, iterando deve ser reinicializado

        # se adicionou elemento, então aumentou o tamanho
        self.__tamanho += 1

    # gerar uma cópia da lista
    def copiar(self):
        return self[:]

    # esvaziar a lista
    def limpar(self):
        # remover as referências para os elementos da lista
        # dessa forma o garbage collector irá limpar assim que conveniente
        atual = self.__primeiro
        while atual is not None:
            removido = atual
            atual = atual.próximo
            removido.próximo = None
            removido.conteúdo = None

        self.__primeiro = None
        self.__último = None
        self.__tamanho = 0
        self.__iterando = None  # modificou a lista, iterando deve ser reinicializado

    # reverter a lista
    def reverso(self):
        # criar uma cópia da lista atual para montar uma reversa
        _lista = self.copiar()

        self.limpar()

        for e in _lista:
            self.inserir_início(e)
