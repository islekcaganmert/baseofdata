import base64

class Data:
    def create(self, structure):
        data = ''
        for column in structure:
            column_name_check = column.lower()
            for i in 'abcdefghijklmnopqrstuvwxyz1234567890':
                column_name_check = column_name_check.replace(i, '')
            if column_name_check == '':
                if structure[column] in ['String', 'Integer', 'Float', 'Boolean']:
                    data = data + ' ' + structure[column] + ':' + column
        open(self.filename, 'wb').write(b'Info v0.0.1;Config'+data.encode('UTF-8')+b';Data ;')
        self.fetch()
    def commit(self):
        filedata = b'Info v0.0.1;Config'
        for column in self.config:
            column_name_check = column.lower()
            for i in 'abcdefghijklmnopqrstuvwxyz1234567890':
                column_name_check = column_name_check.replace(i, '')
            if column_name_check == '':
                if self.config[column] in ['String', 'Integer', 'Float', 'Boolean']:
                    filedata = filedata + b' ' + self.config[column].encode('UTF-8') + b':' + column.encode('UTF-8')
        filedata+=b';Data '
        for column in self.data:
            for inp in column:
                if not inp == '__id__':
                    if self.config[inp] == 'String': inp_type = str
                    elif self.config[inp] == 'Integer': inp_type = int
                    elif self.config[inp] == 'Float': inp_type = float
                    elif self.config[inp] == 'Boolean': inp_type = bool
                    if type(column[inp]) == inp_type:
                        if self.config[inp] == 'String':
                            encoded_hex_list = [f'\\x{byte:02x}'.encode('UTF-8') for byte in column[inp].encode('utf-8')]
                            filedata+=b''.join(encoded_hex_list)
                        elif self.config[inp] == 'Integer':
                            filedata+=str(column[inp]).encode('UTF-8')
                        elif self.config[inp] == 'Float':
                            filedata+=str(column[inp]).encode('UTF-8')
                        elif self.config[inp] == 'Boolean':
                            if column[inp]:
                                filedata+=b'1'
                            else:
                                filedata+=b'0'
                    else:
                        raise Exception("Data type is not acceptable: "+str(column["__id__"])+"/"+inp)
                    filedata+=b' '
        filedata = filedata.removesuffix(b' ') + b';'
        open(self.filename, 'wb').write(filedata)
    def fetch(self):
        config = []
        data = []
        info = {'version':''}
        for block in open(self.filename, 'rb').read().split(b';'):
            if block.startswith(b'Info '):
                info['version'] = block.split(b' ')[1].decode('UTF-8')
        if info['version'] in ['v0.0.1']:
            for block in open(self.filename, 'rb').read().split(b';'):
                if block.startswith(b'Config '):
                    for configblock in block.removeprefix(b'Config ').split(b' '):
                        config.append([configblock.split(b':')[1].decode('UTF-8'), configblock.split(b':')[0].decode('UTF-8')])
                elif block.startswith(b'Data '):
                    i = 0
                    c = 0
                    cd = {'__id__':c}
                    if not block == b'Data ':
                        for datablock in block.removeprefix(b'Data ').split(b' '):
                            if config[i][1] == 'String':
                                encoded_hex_list = datablock.decode('ASCII').split('\\x')
                                encoded_bytes = bytes.fromhex(''.join(encoded_hex_list))
                                conv_data = encoded_bytes.decode('utf-8')
                            elif config[i][1] == 'Integer': conv_data = int(datablock.decode('UTF-8'))
                            elif config[i][1] == 'Float': conv_data = float(datablock.decode('UTF-8'))
                            elif config[i][1] == 'Boolean': conv_data = bool(int(datablock.decode('UTF-8')))
                            cd.update({config[i][0]:conv_data})
                            if len(config)-1 == i:
                                data.append(cd)
                                i = 0
                                c += 1
                                cd = {'__id__':c}
                            else:
                                i+=1
        self.data = data
    def add(self, **data):
        self.fetch()
        filedata = open(self.filename, 'rb').read()
        fileblocks = filedata.split(b';')
        filedatablock = b''
        for fileblock in fileblocks:
            if fileblock.startswith(b'Data '):
                filedatablock = fileblock
        newdata = b' '
        for inp in self.config:
            if self.config[inp] == 'String': inp_type = str
            elif self.config[inp] == 'Integer': inp_type = int
            elif self.config[inp] == 'Float': inp_type = float
            elif self.config[inp] == 'Boolean': inp_type = bool
            if type(data[inp]) == inp_type:
                if self.config[inp] == 'String':
                    encoded_hex_list = [f'\\x{byte:02x}'.encode('UTF-8') for byte in data[inp].encode('utf-8')]
                    newdata+=b''.join(encoded_hex_list)
                elif self.config[inp] == 'Integer':
                    newdata+=str(data[inp]).encode('UTF-8')
                elif self.config[inp] == 'Float':
                    newdata+=str(data[inp]).encode('UTF-8')
                elif self.config[inp] == 'Boolean':
                    if data[inp]:
                        newdata+=b'1'
                    else:
                        newdata+=b'0'
            else:
                raise Exception("Data type is not acceptable")
            newdata+=b' '
        filedata = filedata.replace(filedatablock, (filedatablock+newdata.removesuffix(b' ')).replace(b'  ', b' '))
        open(self.filename, 'wb').write(filedata)
        self.fetch()
    def edit(self, __id__, **datas):
        self.fetch()
        for data in datas:
            self.data[__id__][data] = datas[data]
        self.commit()
        self.fetch()
    def remove(self, id):
        self.fetch()
        newdata = []
        for data in self.data:
            if not data['__id__'] == id:
                newdata.append(data)
        self.data = newdata
        self.commit()
    def get(self, **filters):
        columns = self.data
        results = []
        for i in filters:
            for column in columns:
                if column[i] == filters[i]:
                    if not column in results:
                        results.append(column)
        return results
    def __init__(self, filename):
        self.filename = filename
        self.config = {}
        self.data = []
        try:
            self.fetch()
            info = {'version':''}
            for block in open(self.filename, 'rb').read().split(b';'):
                if block.startswith(b'Info '):
                    info['version'] = block.split(b' ')[1].decode('UTF-8')
            if info['version'] in ['v0.0.1']:
                for block in open(self.filename, 'rb').read().split(b';'):
                    if block.startswith(b'Config '):
                        self.config = {}
                        for configblock in block.removeprefix(b'Config ').split(b' '):
                            self.config.update({configblock.split(b':')[1].decode('UTF-8'): configblock.split(b':')[0].decode('UTF-8')})
        except:
            pass