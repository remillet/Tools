use strict;

while (<>) {
  chomp;
  s/\r//g;
  my (@columns) = split "\t",$_,-1;
  #my ($Y,$M,$D) = split '-',$columns[6];
  @columns[6] .= "T00:00:00Z" if @columns[6];
  #print scalar @columns, "\n";
  print join("\t",@columns). "\n";
}

