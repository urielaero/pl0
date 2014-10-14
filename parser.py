#!/usr/bin/python
import sys
from scanner import scanner

#TODO ver que pedo con el arbol
class Nodo(object):
    def __init__(self,objActual):
        self.nombre = objActual.nombre()
        self.token = objActual.token.token

    def agregarHijo(self,padre,nodo):
        nodo.pi = padre
        self.ramas = []

    def agregarSiguiente(self,nodo):
        nodo.ramas.append(nodo)
        
    

class Token(object):
    def __init__(self,nombreArchivo):
        self.tokens = scanner(nombreArchivo)
        if not self.tokens:
            print "Error al ejecutar el scanner"
            exit(1)
        #print [i.token for i in self.tokens]
        self.index = -1
        self.token = None
        self.avanzar = False
        self.nodo = None

    def permitirSiguiente(self):
        self.avanzar = True

    def siguiente(self):
        if self.avanzar:
            self.avanzar = False
            self.index += 1
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]
            return self.token.tipo

    def regresa(self):
        if self.avanzar:
            self.avanzar = False
            self.index -= 1
        if self.index > -1:
            self.token = self.tokens[self.index]
            return self.token.tipo

    def makeError(self,debe):
        #uno antes para indicar
        token = self.tokens[self.index-1]
        token.infoError("se esperaba "+debe+" se encontro "+self.token.tipo)

    def objeto(self):
        return self.token


class Parser(object):
    def __init__(self,tokens,nodo = False):
        self.token = tokens
        if nodo != False:
            self.nodo = nodo
        else:
            self.nodo = []

    def parse(self):
        self.token.nodo = Nodo(self)
        p = Program(self.token)
        if p.parse():
            self.nodo.append(p)
   
    def nombre(self):
        return type(self).__name__
   
    def imprimir(self,indent = 0):
        for i in self.nodo:
            for j in range(indent):
                print "    ",
                if not j==indent-1:
                    print "|",
            if indent:
                print "+-----",
            print i.nombre()
            if hasattr(i,'imprimir'):
                i.imprimir(indent+1)


class Program(Parser):
    def parse(self):
        bloque = Bloque(self.token)
        bloque.parse()
        self.token.permitirSiguiente()
        if  self.token.siguiente() == 'token_punto':
            self.nodo.append(bloque)
            print "excelente codigo"
            return True
        else:
            self.token.makeError('"." al final')

class Bloque(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()
        res = False
        if t == 'token_const':
            const = SeccionConst(self.token)
            res = const.parse()
            if res:
                self.nodo.append(const)
                self.token.permitirSiguiente()
                t = self.token.siguiente()

        if t == 'token_var':
            var = SeccionVar(self.token)
            res = var.parse()
            if res:
                self.nodo.append(var)
                self.token.permitirSiguiente()
                t = self.token.siguiente()

        while t == 'token_procedure' and res:
            procedure = SeccionProcedure(self.token)
            res = procedure.parse()
            if res:
                self.nodo.append(procedure)
                #t = self.token.token.tipo
                self.token.permitirSiguiente()
                t = self.token.siguiente()
        
        if res:
            #self.token.permitirSiguiente()
            instruccion = Instruccion(self.token)
            res = instruccion.parse()
            if res:
                self.nodo.append(instruccion)
        else:
            print "mal antes statement!",t
            exit(1)
        return res

class SeccionConst(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()
        if t == 'token_id':
            self.nodo.append(self.token.objeto())
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_igual':
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if t == 'token_numero':
                    self.nodo.append(self.token.objeto())
                    self.token.permitirSiguiente()
                    t = self.token.siguiente()
                    if t == 'token_coma':
                        masId = SeccionConst(self.token,self.nodo)
                        return masId.parse()
                    elif t == 'token_punto_coma':
                        return True
                    else:
                        if t == 'token_id':
                            self.token.makeError(",")
                        else:
                            self.token.makeError(";")
                            

                else:
                    self.token.makeError("numero")
            else:
                self.token.makeError("igual")
        else:
            self.token.makeError("[SeccionConst]identificador")
        return False
            
class SeccionVar(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()
        if t == 'token_id':
            self.nodo.append(self.token.objeto())
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_coma':
                masId = SeccionVar(self.token,self.nodo)
                #self.nodo.append(self)
                return masId.parse()
            elif t == 'token_punto_coma':
                return True
            else:
                self.token.makeError('; o ,')
        else:
            self.token.makeError('[SeccionVar] identificador')
        return False

class SeccionProcedure(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()

        if t == 'token_id':
            self.nodo.append(self.token.objeto())
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_punto_coma':
                bloque = Bloque(self.token)
                if bloque.parse():
                    self.nodo.append(bloque)
                    self.token.permitirSiguiente()
                    t = self.token.siguiente()
                    if t == 'token_punto_coma':
                        return True
                    else:
                        self.token.makeError("';'1")
                    
            else:
                self.token.makeError("';'")
        else:
            self.token.makeError("[SeccionProcedure] identificador")

        return False
      
class Instruccion(Parser):
    def parse(self):
        #self.token.permitirSiguiente()
        t = self.token.siguiente()

        if t == 'token_id':
            self.nodo.append(self.token.objeto())
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_asignacion':
                #self.nodo.append(self.token.objeto())
                expresion = Expresion(self.token)
                res = expresion.parse()
                self.nodo.append(expresion)
                return res

        elif t == 'token_call':
            self.nodo.append(self.token.objeto())
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_id':
                return True
        elif t == 'token_begin':
            seguir = True
            while True:
                self.token.permitirSiguiente()
                instruccion = Instruccion(self.token,self.nodo)
                res = instruccion.parse()
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if res and t == 'token_punto_coma':
                    #; sigue
                    self.token.permitirSiguiente()
                    t2 = self.token.siguiente()
                    if t2 == 'token_end':
                        return True
                    
                    self.token.permitirSiguiente()
                    self.token.regresa()
                        
                elif res and t == 'token_end':
                    return True
                else:
                    self.token.makeError('[Instrucion] ";" o end')
                    return False
        
        elif t == 'token_if':
            condicion = Condicion(self.token)
            if condicion.parse():
                self.nodo.append(condicion)
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if t == 'token_then':
                    self.token.permitirSiguiente()
                    instruccion = Instruccion(self.token,self.nodo)
                    if instruccion.parse():
                        return True
                    else:
                        self.token.makeError('[instruccion-if] ')
        elif t == 'token_while':
            #self.token.permitirSiguiente()
            #t = self.token.siguiente()
            condicion = Condicion(self.token)
            if condicion.parse():
                self.nodo.append(condicion)
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if t == 'token_do':
                    self.token.permitirSiguiente()
                    instruccion = Instruccion(self.token,self.nodo)
                    if instruccion.parse():
                        return True
        else:
            self.token.makeError('[Instruccion]')
        return False

#TODO quitar
class Statement(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()
        if t == 'token_id' and res:
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_asignacion':
                expresion = Expresion(self.token)
                res = expresion.parse()
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if t == 'token_punto_coma':
                    pass
                    #este lo gestiona el de begin []
                    #return res
                else:
                    self.token.makeError(';')
                    res = False
                #return res
            else:
                self.token.makeError('":="')
                return False
        
        if t == 'token_call' and res:
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_id':
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                #return True
            else:
                self.token.makeError('id')
        
        if t == 'token_begin' and res:
            res2 = True
            while res and res2:

                masStatement = Statement(self.token)
                res =  masStatement.parse()

                self.token.permitirSiguiente()
                t = self.token.siguiente()

                if res and t != 'token_end' and t == 'token_punto_coma':
                    self.token.permitirSiguiente()
                    t = self.token.siguiente()
                elif t == 'token_end':
                    self.permitirSiguiente()
                    t = self.token.siguiente()
                    res2 = False #termina bucle
                else:
                    self.token.makeError('end o ";"')
                    return False
            if not res:
                return False
        
        if t == 'token_if' and res:
            condicion = Condicion(self.token)
            res = condicion.parse()
            if res:
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if t == 'token_then':
                    masStatement = Statement(self.token)
                    res = masStatement.parse()
                    self.token.permitirSiguiente()
                    t = self.token.siguiente()
                    #return res
                else:
                    self.token.makeError('then')
                    return False
        
        if t == 'token_while' and res:
            condicion = Condicion(self.token)
            res = condicion.parse()
            if res:
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if t == 'token_do':
                    masStatement = Statement(self.token)
                    res = masStatement.parse()
                    if res:
                        self.token.permitirSiguiente()
                        t = self.token.siguiente()
                    #return res
                else:
                    self.token.makeError('do')
                    return False
            else:
                return False

        if res and t in [
                            'token_id',
                            'token_call',
                            'token_begin',
                            'token_if',
                            'token_while',
                        ]:
            masStatement = Statement(self.token)
            res = masStatement.parse()
            
        else:
            return res

class Condicion(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()
        if t == 'token_odd':
            self.nodo.append(self.token.objeto())
            expresion = Expresion(self.token)
            self.nodo.append(expresion)
            return expresion.parse()
        
        self.token.permitirSiguiente()
        self.token.regresa()

        expresion = Expresion(self.token)
        res = expresion.parse()
        if res:
            self.nodo.append(expresion)
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t in [
                        'token_igual',
                        'token_distinto',
                        'token_menor',
                        'token_mayor',
                        'token_menor_igual',
                        'token_mayor_igual'
                    ]:
                    
                expresion = Expresion(self.token)
                self.nodo.append(expresion)
                res = expresion.parse()
            else:
                self.token.makeError('= o <> o < o > o <= o !=')
        
        return res

class Expresion(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()
        if t in ['token_suma','token_resta']:
            self.nodo.append(self.token.objeto())
            self.token.permitirSiguiente()
            self.token.siguiente()

        term = Term(self.token)
        res = term.parse()
        
        self.nodo.append(term)

        self.token.permitirSiguiente()
        t = self.token.siguiente()

        while res and t in ['token_suma','token_resta']:
            self.nodo.append(self.token.objeto())
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            term = Term(self.token)
            res = term.parse()
            self.nodo.append(term)

            self.token.permitirSiguiente()
            t = self.token.siguiente()

        if res:
            self.token.permitirSiguiente()
            self.token.regresa()

        return res
        
#TODO quitar este:
class Expresion2(Parser):
    def parse(self):
        self.token.permitirSiguiente()
        t = self.token.siguiente()
        while t == 'token_suma' or t == 'token_resta':
            self.token.permitirSiguiente()
            t = self.token.siguiente()
        term = Term(self.token)
        res = term.parse()
        if res:
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            while res and t in ['token_suma','token_resta']:
                self.token.permitirSiguiente()
                t = self.token.siguiente()
            self.token.permitirSiguiente()
            self.token.regresa()

        return res
        """
        if res:
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            while res and t in ['token_suma','token_resta']:
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                term = Term(self.token)
                res = term.parse()
            return res
        return False
        """

class Term(Parser):
    def parse(self):
        factor = Factor(self.token)
        res = factor.parse()
        self.nodo.append(factor)
        if res:
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            while res and t in ['token_mul','token_div']:
                self.nodo.append(self.token.objeto())
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                otroFactor = Factor(self.token)
                res = otroFactor.parse()
                self.nodo.append(otroFactor)

                self.token.permitirSiguiente()
                t = self.token.siguiente()
           
            self.token.permitirSiguiente()
            self.token.regresa()
            
        return res

        """
        while res:
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t in ['token_mul','token_div']:
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                factor = Factor(self.token)
                res = factor.parse()
            else:
                print 'Term',self.token.token.tipo
                self.token.permitirSiguiente()
                self.token.regresa()
                print 'Term',self.token.token.tipo
                return True
        return res
        """
class Factor(Parser):
    def parse(self):
        t = self.token.token.tipo
        if t in ['token_id','token_numero']:
            self.nodo.append(self.token.objeto())
            return True
        elif t == 'token_apertura_de_parentesis':
            self.nodo.append(self.token.objeto())
            expresion = Expresion(self.token)
            res = expresion.parse()
            if res:
                self.nodo.append(expresion)
                self.token.permitirSiguiente()
                t = self.token.siguiente()
                if t == 'token_cierre_parentesis':
                    self.nodo.append(self.token.objeto())
                    return True
                else:
                    self.token.makeError("cierre de parentesis")
        else:
            self.token.makeError('[Factor] identificador o numero o "("')
        return False



if __name__=="__main__":
    if len(sys.argv) == 2:
        tokens = Token(sys.argv[1])
        p = Parser(tokens)
        p.parse()
        p.imprimir()
    else:
        print "uso: ",sys.argv[0]," nombreArchivo.pl0"
"""
raiz = Nodo("raiz")
hijo1 = Nodo("un hijo")
hijo2 = Nodo("un siguiente")

raiz.agregar(hijo1)
raiz.agregar(hijo2)

n = hijo1
while(n.pi != None):
    n = n.pi
    print n.test
"""
