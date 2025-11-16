class Entry:
    # Código trabajado en clase pasado a lenguaje python, sin cambios
    def __init__(self, key: str, value: int):
        self._key = key
        self._value = value
        self._isDeleted = False

class HashTable:
    # Código trabjado en clase pasado a lenguaje python, solo con la implementación de una nueva variable
    def __init__(self, size=5):
        self.__size = size
        self.__bins = [None] * size
        self.__num_keys = 0
        # Se establece el primo menor respecto al tamaño fijo que se ha establecido antes, el cual viene a ser size = 5. Esto se debe a que
        # el double hashing recomienda que sea así para que el salto que se hará sea un recorrido dentro de la tabla.
        self.__R = 3

    # Código trabajado de hashFunction pasado a lenguaje python, sin cambios.
    def hashFunction(self, key: str):
        hash_val = 0
        for c in key:
            hash_val = (hash_val * 31 + ord(c)) % self.__size
        return hash_val

    # Función hashFunction2 que ayuda a determinar el salto que dará por la clave que se ingresará y extraído del libro de Weiss descrito textualmente
    def hashFunction2(self, key: str):
        hash_val = 0
        # Se usará otro primo diferente respecto al hashFunction para que devuelva un valor diferente,
        # en este caso se usará un valor de 17
        for c in key:
            hash_val = (hash_val * 17 + ord(c)) % self.__size
        # Se halla el valor del salto que dará por la clave que se ingresará
        step = self.__R - (hash_val % self.__R)
        # Si en caso el valor del salto es 0, entonces se cambiará por el valor de 1, ya que el double hashing establece la restricción que el salto
        # no puede ser 0.
        if step == 0:
            step = 1
        return step

    # Función find que cumple el mismo objetivo del libro de Weiss donde se adaptó el double hashing (descrito textualmente), el cual
    # busca determinar la posición de la clave pero mediante el step.
    def find(self, key: str):
        index = self.hashFunction(key)
        step  = self.hashFunction2(key)
        count = 0

        while self.__bins[index] is not None and not self.__bins[index]._isDeleted and self.__bins[index]._key != key and count < self.__size:
            index = (index + step) % self.__size
            count += 1

        return index

    # Función insert que fue adaptado del libro de Weiss, el cual buscar insertar o actualizar un valor.
    def insert(self, key: str, value: int):
        # Llama a la función find para determinar la posición de la clave.
        pos = self.find(key)

        # En caso la posición no esté ocupada, entonces se insertará la llave con su valor.
        if self.__bins[pos] is None or self.__bins[pos]._isDeleted:
            self.__bins[pos] = Entry(key, value)
            self.__num_keys += 1
        # Caso contrario, se actualizará el valor
        else:
            self.__bins[pos]._value = value

        return True

    #La función lookup fue modificada para que haga los saltos establecidos en cada llave.
    def lookup(self, key: str):
        index = self.hashFunction(key)
        step = self.hashFunction2(key)
        count = 0

        while self.__bins[index] is not None and count < self.__size:
            if not self.__bins[index]._isDeleted and self.__bins[index]._key == key:
                return self.__bins[index]._value
            # En vez de sumar + 1 como el código base, sumará con el salto
            index = (index + step) % self.__size
            count += 1
        return None

    # Código imprimir trabajado en clase pasado a lenguaje python, con la única modificación que se adapte a un jugador.
    def imprimir(self, nombre):
        print(f"HABILIDADES DE {nombre.upper()}: ")
        for index in range(self.__size):
            print(f"[{index}]: ", end = "")
            if self.__bins[index] is None:
                print("null")
            elif self.__bins[index]._isDeleted:
                print("deleted")
            else:
                print(f"({self.__bins[index]._key}, {self.__bins[index]._value})")
        print()