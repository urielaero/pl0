#!/usr/bin/python
import sys
from scanner import scanner

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
        exit(1)

    def objeto(self):
        return self.token


class Parser(object):

    varId = []
    const = []
    etiquetasDict = {
        'etiquetaFinalActual':[],
        'etiquetaInicioActual':[],
        'while':0,
        'if':0
    }

    def __init__(self,tokens,nodo = False):
        self.token = tokens
        if nodo != False:
            self.nodo = nodo
        else:
            self.nodo = []


    def parse(self):
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
    
    #def traducir(self,indice=0):
    #    return self.traducirNodo(indice)

    def traducirNodos(self,indice):
        for i in self.nodo:
            if hasattr(i,'traducir'):
                i.traducir(indice)
    
    def getLevelVarId(self,indice,name):
        last = False
        mejor = self.varId[0]
        for i in self.varId:
            tId = i.get("token",False)
            lId = i.get("nivel")
            if tId and tId == name and lId <= indice:
                if not last or i["nivel"] >= last["nivel"]:
                    last = i
        var = True
        if not last:
            var = False
            for i in self.const:
                tId = i.get(name,False)
                lId = i.get("nivel")
                if tId!=False and lId <= indice:
                    if not last or i["nivel"] >= last["nivel"]:
                        last = i
            return tId,False
                
        nivel = indice - last["nivel"]
        return nivel,var
        #if not last ERROR no id

    def getEtiquetaFinal(self):
        ets = self.etiquetasDict['etiquetaFinalActual']
        if len(ets):
            et = ets.pop()
            #,et[:-1]
            if et[-1] == ':':
                return et[:-1]
            return et
        #error

    def getEtiquetaInicio(self):
        ets = self.etiquetasDict['etiquetaInicioActual']
        if len(ets):
            et = ets.pop()
            print "sadasda!!!!!!!!!!!!!!!!!!!!"
            if et[-1] == ':':
                return et[:-1]
            return et
        #error

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

    def traducir(self,indice):
        print "Program ",indice
        return super(Program,self).traducirNodos(indice)

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
            instruccion = Instruccion(self.token,self.nodo)
            res = instruccion.parse()
            if res:
	    	pass
                #self.nodo.append(instruccion)
        else:
            print "mal antes statement!",t
            exit(1)
        return res

    def traducir(self,indice):
        print "Bloque ",indice
        return super(Bloque,self).traducirNodos(indice+1)

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

    def traducir(self,indice):
        print "Const ",indice
        #print dir(self)
        dic = {}
        
        for i,nodo in enumerate(self.nodo):
            val = nodo.token;
            if i%2 == 0:
                back = val
            else:
                dic[back] = val
                

        dic['nivel'] = indice
        self.const.append(dic)
        return super(SeccionConst,self).traducirNodos(indice)
            
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

    def traducir(self,indice):
        print "Var ",indice
        print "INS {} {} ;allocate!".format(indice,len(self.nodo)+3)
        for nodo in self.nodo:
            self.varId.append({"nivel":indice,"token":nodo.token})
        
        return super(SeccionVar,self).traducirNodos(indice)

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

    def traducir(self,indice):
        print "Procedure ",indice
        procedureName = self.nodo[0].token
        print "INICIO{}:".format(procedureName)
        super(SeccionProcedure,self).traducirNodos(indice)
        print "OPR 0,0"
      
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
            nodoCall = self.token.objeto()
            #self.nodo.append(nodoCall)
            self.token.permitirSiguiente()
            t = self.token.siguiente()
            if t == 'token_id':
                nodoCall.val = self.token.objeto()
                self.nodo.append(nodoCall)
                return True
        elif t == 'token_begin':
            seguir = True
            while True:
                self.token.permitirSiguiente()
                instruccion = Instruccion(self.token)
                res = instruccion.parse()
                self.nodo.append(instruccion)
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
            iF = If(self.token)
            res = iF.parse()
            if res:
                self.nodo.append(iF)
                return res
            """
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
            """
        elif t == 'token_while':
            #self.token.permitirSiguiente()
            #t = self.token.siguiente()
            w = While(self.token)
            res = w.parse()
            if res:
                self.nodo.append(w)
                return res

        else:
            self.token.makeError('[Instruccion]')
        return False

    def traducir(self,indice):
        super(Instruccion,self).traducirNodos(indice)
        for nodo in self.nodo:
            if hasattr(nodo,"tipo"):
                tId = nodo.token
                if nodo.tipo == 'token_id':
                    identId,var = self.getLevelVarId(indice,nodo.token)
                    if var:
                        print "ALM {} {}".format(identId,nodo.token)
                elif nodo.tipo == 'token_call':
                    print "LLA 0,INICIO{}".format(nodo.val.token)

class If(Parser):
    def parse(self):
        self.nodo.append(self.token.objeto())
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

    def traducir(self,indice):
        #print "While ",indice
        self.etiquetasDict["if"] += 1
        ifName = self.etiquetasDict['if']
        #print "INICIAIF_{}:".format(ifName)
        ifFinal = "TERMINAIF_{}:".format(ifName)
        self.etiquetasDict['etiquetaFinalActual'].append(ifFinal)
        super(If,self).traducirNodos(indice)
        print ifFinal

class While(Parser):
    def parse(self):
        self.nodo.append(self.token.objeto())
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

    def traducir(self,indice):
        #print "While ",indice
        self.etiquetasDict["while"] += 1
        whileName = self.etiquetasDict['while']
        whileInicia = "INICIAWHILE_{}:".format(whileName)
        print whileInicia
        whileFinal = "TERMINAWHILE_{}:".format(whileName)
        self.etiquetasDict['etiquetaFinalActual'].append(whileFinal)
        super(While,self).traducirNodos(indice)
        print "SAL 0,",whileInicia[:-1]
        print whileFinal

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

                self.nodo.append(self.token.objeto())               
                expresion = Expresion(self.token)
                self.nodo.append(expresion)
                res = expresion.parse()
            else:
                self.token.makeError('= o <> o < o > o <= o !=')
        
        return res

    def traducir(self,indice):
        super(Condicion,self).traducirNodos(indice)
        for nodo in self.nodo:
            if hasattr(nodo,'tipo'):
                print "OPR 0,",nodo.token
                print "SAC 0,",self.getEtiquetaFinal()

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

    def traducir(self,indice):
        #print "Expresion !!!!!!!",indice
        super(Expresion,self).traducirNodos(indice)
        for nodo in self.nodo:
            if hasattr(nodo,'tipo'):
                print "OPR 0",nodo.token
        
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
    def traducir(self,indice):
        #print "Term !!!!!!!",indice
        super(Term,self).traducirNodos(indice)
        for nodo in self.nodo:
            if hasattr(nodo,'tipo'):
                print "OPR 0,",nodo.token

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

    def traducir(self,indice):
        fac =  self.nodo[0]
        if fac.tipo == 'token_id':
            facId,var = self.getLevelVarId(indice,fac.token)
            if var:
                print "CAR {},{}".format(facId,fac.token)
            else:
                print "LIT 0,{}".format(facId)
        elif fac.tipo == 'token_numero':
            print "LIT 0,{}".format(fac.token)
        super(Factor,self).traducirNodos(indice)

def parse(nombreArchivo):
    tokens = Token(nombreArchivo)
    p = Parser(tokens)
    p.parse()
    return p


if __name__=="__main__":
    if len(sys.argv) == 2:
        p = parse(sys.argv[1])
        p.imprimir()
        p.traducirNodos(-1)
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
