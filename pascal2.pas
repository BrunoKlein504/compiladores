program Exemplo1;
var
  fat, num, cont: integer;
begin
  read(num);
  fat := 1;
  cont := 2;
  while cont <= num do
  begin
    fat := fat * cont;
    cont := cont + 1;
  end;
  write(fat);
end.