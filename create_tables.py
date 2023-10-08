


class CreateTables:

    def __init__(self):
        pass

    def aaa(self):
        with open('create_tables.sql', 'r') as f:
            content = f.read()

        breakpoint()
        print("aaa")


if __name__ == '__main__':

    abc = CreateTables()
    abc.aaa()