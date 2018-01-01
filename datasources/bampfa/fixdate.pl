use strict;

while (<>) {
  chomp;
  my (@columns) = split "\t",$_,-1;
  @columns[7] .= "T00:00:00Z" if @columns[7];
  @columns[25] =~ s/ /T/;
  @columns[25] .= 'Z';
  print join("\t",@columns). "\n";
}

