```
const m = 7, otro = 85;
var x, y, z, q, r;

procedure multiply;
  var a,b;
begin 
    a := +1;
    b := (2+1*2);
    c := 1;
end;

procedure gcd;
  var f,g;
begin	f := x; g := y;
	while f <> g do
	begin	if f < g then g := g - f;
		if g < f then f := f - g;
	end;
	z := f
end;

begin
	x :=  m; y :=  n;
end.

excelente codigo

Program
     +----- Bloque
     |      +----- SeccionConst
     |      |      +----- token_id  'm '
     |      |      +----- token_numero  '7'
     |      |      +----- token_id  'otro '
     |      |      +----- token_numero  '85'
     |      +----- SeccionVar
     |      |      +----- token_id  'x'
     |      |      +----- token_id  'y'
     |      |      +----- token_id  'z'
     |      |      +----- token_id  'q'
     |      |      +----- token_id  'r'
     |      +----- SeccionProcedure
     |      |      +----- token_id  'multiply'
     |      |      +----- Bloque
     |      |      |      +----- SeccionVar
     |      |      |      |      +----- token_id  'a'
     |      |      |      |      +----- token_id  'b'
     |      |      |      +----- Instruccion
     |      |      |      |      +----- token_id  'a '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- token_suma  '+'
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_numero  '1'
     |      |      |      |      +----- token_id  'b '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_apertura_de_parentesis  '('
     |      |      |      |      |      |      |      +----- Expresion
     |      |      |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      |      |      +----- token_numero  '2'
     |      |      |      |      |      |      |      |      +----- token_suma  '+'
     |      |      |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      |      |      +----- token_numero  '1'
     |      |      |      |      |      |      |      |      |      +----- token_mul  '*'
     |      |      |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      |      |      +----- token_numero  '2'
     |      |      |      |      |      |      |      +----- token_cierre_parentesis  ')'
     |      |      |      |      +----- token_id  'c '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_numero  '1'
     |      +----- SeccionProcedure
     |      |      +----- token_id  'gcd'
     |      |      +----- Bloque
     |      |      |      +----- SeccionVar
     |      |      |      |      +----- token_id  'f'
     |      |      |      |      +----- token_id  'g'
     |      |      |      +----- Instruccion
     |      |      |      |      +----- token_id  'f '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_id  'x'
     |      |      |      |      +----- token_id  'g '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_id  'y'
     |      |      |      |      +----- Condicion
     |      |      |      |      |      +----- Expresion
     |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      +----- token_id  'f '
     |      |      |      |      |      +----- Expresion
     |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      +----- token_id  'g '
     |      |      |      |      +----- Condicion
     |      |      |      |      |      +----- Expresion
     |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      +----- token_id  'f '
     |      |      |      |      |      +----- Expresion
     |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      +----- token_id  'g '
     |      |      |      |      +----- token_id  'g '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_id  'g '
     |      |      |      |      |      +----- token_resta  '-'
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_id  'f'
     |      |      |      |      +----- Condicion
     |      |      |      |      |      +----- Expresion
     |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      +----- token_id  'g '
     |      |      |      |      |      +----- Expresion
     |      |      |      |      |      |      +----- Term
     |      |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      |      +----- token_id  'f '
     |      |      |      |      +----- token_id  'f '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_id  'f '
     |      |      |      |      |      +----- token_resta  '-'
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_id  'g'
     |      |      |      |      +----- token_id  'z '
     |      |      |      |      +----- Expresion
     |      |      |      |      |      +----- Term
     |      |      |      |      |      |      +----- Factor
     |      |      |      |      |      |      |      +----- token_id  'f'
     |      +----- Instruccion
     |      |      +----- token_id  'x '
     |      |      +----- Expresion
     |      |      |      +----- Term
     |      |      |      |      +----- Factor
     |      |      |      |      |      +----- token_id  'm'
     |      |      +----- token_id  'y '
     |      |      +----- Expresion
     |      |      |      +----- Term
     |      |      |      |      +----- Factor
     |      |      |      |      |      +----- token_id  'n'
```
