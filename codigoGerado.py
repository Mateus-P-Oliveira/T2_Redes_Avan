import MySQLdb
import tools.tools

# Classe para armazenar configurações do banco de dados
class DatabaseConfig:
    def __init__(self, addr, user, password):
        self.ADDR = addr
        self.USER = user
        self.PASS = password


class comunidades:
    def __init__(self, BBDD):
        self.BBDD = BBDD

    def get(self, oid):
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = ""
        exito_resp = 1

        if len(suboid) == 9 or len(suboid) > 11:
            db_comunidades = MySQLdb.connect(host=self.BBDD.ADDR, user=self.BBDD.USER, passwd=self.BBDD.PASS, db="comunidades")
            db_comunidades.autocommit(True)
            cursor = db_comunidades.cursor()

            cursor.execute("SELECT next_table, value FROM ts_comunidades WHERE orden = %s", (suboid[7],))
            result = cursor.fetchone()
            if result:
                next_table, value = result
                if str(next_table) == 'nextTable':
                    val_resp = value
                else:
                    cname = ''.join(chr(int(i)) for i in suboid[10:len(suboid)-1])
                    sKey = suboid[-1]
                    pKey = '.'.join(suboid[10:len(suboid)-1])

                    cursor.execute("SELECT name, next_table, indices, type_value, access FROM " + next_table + " WHERE orden = %s", (suboid[9],))
                    result = cursor.fetchone()
                    if result:
                        name, next_table, indice, type2_resp, access = result

                        if access in [1, 3]:  # Access check
                            cursor.execute(f"SELECT {name} FROM {next_table} WHERE communityIndex = %s and id = %s", (pKey, sKey))
                            result = cursor.fetchone()
                            if result:
                                val_resp = result[0]
                            else:
                                exito_resp = 0
                        else:
                            exito_resp = 0
                    else:
                        exito_resp = 0
            else:
                exito_resp = 0
        else:
            exito_resp = 0

        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp

    def getnext(self, oid):
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = ""
        exito_resp = 1

        if tools.tools.menor_que(oid, '1.3.6.1.4.1.28308.1.0'):
            oid_resp = "1.3.6.1.4.1.28308.1.0"
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(oid_resp)
        else:
            if tools.tools.menor_que(oid, '1.3.6.1.4.1.28308.2'):
                suboid = ['1', '3', '6', '1', '4', '1', '28308', '2']

            if len(suboid) < 10:
                suboid += ['1', '1']
            if len(suboid) < 11:
                suboid.append('0')
            if len(suboid) < 12:
                suboid.append('0')

            db_comunidades = MySQLdb.connect(host=self.BBDD.ADDR, user=self.BBDD.USER, passwd=self.BBDD.PASS, db="comunidades")
            db_comunidades.autocommit(True)
            cursor = db_comunidades.cursor()

            while oid_resp == oid and suboid != ['1', '3', '6', '1', '4', '1', '28309', '0', '0']:
                cname = ''.join(chr(int(i)) for i in suboid[10:len(suboid)-1])
                sKey = suboid[-1]
                pKey = '.'.join(suboid[10:len(suboid)-1])

                cursor.execute("SELECT next_table FROM ts_comunidades WHERE orden = %s", (suboid[7],))
                result = cursor.fetchone()
                if result:
                    tc_table = result[0]
                    cursor.execute(f"SELECT next_table, indices FROM {tc_table} WHERE orden = %s", (suboid[9],))
                    result = cursor.fetchone()
                    if result:
                        td_table, indice = result
                        cursor.execute(f"SELECT communityIndex, id FROM {td_table} WHERE communityName = %s and id > %s ORDER BY communityName ASC, id ASC", (cname, sKey))
                        result = cursor.fetchone()
                        if result:
                            suboid_resp = suboid[:10] + result[0].split('.') + [str(int(result[1]))]
                            oid_resp = '.'.join(suboid_resp)
                        else:
                            cursor.execute(f"SELECT communityIndex, id FROM {td_table} WHERE communityName > %s ORDER BY communityName ASC, id ASC", (cname,))
                            result = cursor.fetchone()
                            if result:
                                suboid_resp = suboid[:10] + result[0].split('.') + [str(int(result[1]))]
                                oid_resp = '.'.join(suboid_resp)
                            else:
                                cursor.execute(f"SELECT next_oid FROM {tc_table} WHERE orden = %s", (suboid[9],))
                                result = cursor.fetchone()
                                if result:
                                    suboid = str(result[0]).split('.') + ['0', '0']
                if oid_resp == oid:
                    exito_resp = 0
                else:
                    exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(oid_resp)

        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp

    def set(self, oid, val):
        suboid = str(oid).split('.')
        type1_resp = "ObjectName"
        type2_resp = ""
        oid_resp = oid
        val_resp = val
        exito_resp = 1

        if len(suboid) > 9:
            if suboid[9] == '5':
                subval = val.split('.')
                if not subval[0]:
                    subval = subval[1:]
                if len(subval) == 1:
                    exito_resp = 0

        if (len(suboid) == 9 or len(suboid) > 11) and exito_resp == 1:
            db_comunidades = MySQLdb.connect(host=self.BBDD.ADDR, user=self.BBDD.USER, passwd=self.BBDD.PASS, db="comunidades")
            db_comunidades.autocommit(True)
            cursor = db_comunidades.cursor()
            
            cursor.execute("SELECT next_table FROM ts_comunidades WHERE orden = %s", (suboid[7],))
            result = cursor.fetchone()
            if result:
                next_table = result[0]

                if next_table == 'nextTable':
                    cursor.execute("UPDATE ts_comunidades SET value = %s WHERE orden = %s", (val, suboid[7]))
                else:
                    cursor.execute("SELECT name, next_table, indices, type_value, access FROM " + next_table + " WHERE orden = %s", (suboid[9],))
                    result = cursor.fetchone()
                    if result:
                        name, next_table, indice, type2_resp, access = result
                        status_name = cursor.fetchone()[0]

                        cname = ''.join(chr(int(i)) for i in suboid[10:len(suboid)-1])
                        sKey = suboid[-1]
                        pKey = '.'.join(suboid[10:len(suboid)-1])

                        if access > 1:
                            cursor.execute(f"SELECT {status_name} FROM {next_table} WHERE communityIndex = %s and id = %s", (pKey, sKey))
                            aux = cursor.fetchone()
                            if aux:
                                status_val = aux[0]
                                if status_val == "3" and tools.tools.isType(val, type2_resp):
                                    cursor.execute(f"UPDATE {next_table} SET {name} = %s WHERE communityIndex = %s and id = %s", (val, pKey, sKey))
                            else:
                                exito_resp = 0
                        else:
                            exito_resp = 0
            else:
                exito_resp = 0
        else:
            exito_resp = 0

        return exito_resp, type1_resp, oid_resp, type2_resp, val_resp

    def backup(self, oid, triple):
        suboid = str(oid).split('.')
        doble = []
        uni = []

        if suboid[len(suboid)-1] == '0':
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(oid)
            uni.append(oid)
            uni.append(val_resp)
            doble.append(uni)
        else:
            indice = 1
            suboid[len(suboid)-2] = str(indice)
            oid_temp = '.'.join(suboid)
            exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(str(oid_temp))
            while exito_resp != 0:
                uni.append(oid_temp)
                uni.append(val_resp)
                doble.append(uni)
                uni = []
                indice += 1
                suboid[len(suboid)-2] = str(indice)
                oid_temp = '.'.join(suboid)
                exito_resp, type1_resp, oid_resp, type2_resp, val_resp = self.get(str(oid_temp))

            uni = []
            if doble:
                uni.append(doble[-1][0])
                uni.append('2')
            else:
                uni.append(oid)
                uni.append('4')

            doble.insert(0, uni)

        triple.append(doble)
        return triple

    def rollback(self, doble):
        for entry in doble:
            self.set(str(entry[0]), str(entry[1]))

    def permiso(self, comunidad, oid):
        permisos = 0
        coincidencias = 0
        suboid = str(oid).split('.')
        if suboid[0] == "":
            suboid = suboid[1:]

        db_comunidades = MySQLdb.connect(host=self.BBDD.ADDR, user=self.BBDD.USER, passwd=self.BBDD.PASS, db="comunidades")
        db_comunidades.autocommit(True)
        cursor = db_comunidades.cursor()

        cursor.execute("SELECT value FROM ts_comunidades WHERE orden = 1")
        master = cursor.fetchone()[0]
        if (comunidad == master) and (suboid[0:7] == ['1', '3', '6', '1', '4', '1', '28308']):
            permisos = 3
        else:
            cursor.execute("SELECT * FROM td_communityManagement WHERE communityName = %s and communityStatus = 1", (comunidad,))
            result = cursor.fetchall()
            if result:
                for entry in result:
                    permisos_entrada = int(entry[3])
                    oid_entrada = str(entry[4])
                    suboid_entrada = oid_entrada.split('.')
                    if suboid_entrada[0] == "":
                        suboid_entrada = suboid_entrada[1:]

                    if suboid_entrada == suboid[:len(suboid_entrada)] and len(suboid_entrada) > coincidencias:
                        coincidencias = len(suboid_entrada)
                        permisos = permisos_entrada
        return permisos
