program ex01;
var a, b, c: integer;
    i : integer;
begin
   a := 10;
   b := 20;
   c := 30;
   a := 50;
   if a > 10 then
   begin
      write(a + 10);
      write(b + 20);
      write(c + 30);
      read(a, b, c);
      c := a + b * 10 / 5
   end
   else
   begin
      write(a + 20);
      write(b + 30);
      write(c + 40);
      c := b + a * 20
   end;
   i := 0;
   while i < 10 do
       i := i + 1;
   write(i)
end.