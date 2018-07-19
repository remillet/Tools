if (scalar @ARGV != 6) {
  print "\n";
  print "need 6 file arguments:\n";
  print "rewrite_values invalid_values input output column_to_change column_to_update\n";
  print "\n";
  exit(1);
}

($rewrite_values, $invalid_values, $input, $output, $column_to_change, $column_to_update) = @ARGV;

$column_to_change--;
$column_to_update--;

print "\n";
print 'rewrite:     ' . $rewrite_values . "\n";
print 'invalid:     ' . $invalid_values . "\n";
print 'input:       ' . $input . "\n";
print 'output:      ' . $output . "\n";
print 'change col:  ' . ($column_to_change + 1) . "\n";
print 'update col:  ' . ($column_to_update + 1) . "\n";
print "\n";

open(IN, $invalid_values) || die 'could not read '.  $invalid_values;
while(<IN>){
	chomp;
	next if (m/^#/);
        $invalidin++;
	($invalid)=split(/\t/);
	$INVALID{$invalid}=$invalid;
      }
close(IN);

open(IN, $rewrite_values) || die 'could not read '.  $rewrite_values;

while(<IN>){
	chomp;
        next if (m/^#/);
        $rewritein++;
	($rewrite, $replacewith)=split(/\t/);
	#($replacewith, $rewrite)=split(/\t/);
	$REWRITE{$rewrite}=$replacewith;
	$TARGET_VALUES{$replacewith} = $rewrite;
      }
close(IN);

open(OUT, ">$output") || die 'could not write to ' . $output;
open(IN,$input) || die 'could not read ' . $input;

while(<IN>){
	chomp;
	next if (m/^#/);
        $linesin++;
	@cells = split /\t/,$_,-1;
	$source_column = @cells[$column_to_change];
	
	#($Main_Collector,$Coll_Date,$Coll_Num,$Locality,$State_Province,$Barcode_Number,$County,$Country,$ScientificName,$ID_Qualifier,$DeterminedBy,$Det_Date_Display,$Habitat,$Associated_Taxa,$Latitude,$Longitude,$Datum,$Coordinate_Uncertainty_In_Meters,$Coordinate_Source,$Coordinate_Details,$Elevation,$Elevation_Units,$Cultivated,$Coll_Year,$Coll_Month,$Coll_Day,$Comments,$All_Collectors,$GUID,$Other_Number)=split(/\t/);

#do this first to convert all full name invalid to postal codes
if ($source_column ne ''){
	if (! $TARGET_VALUES{$source_column}){
		$invalid_change = $REWRITE{$source_column};
		#print "$source_column==>$invalid_change\n";
	}
	else{
	$invalid_change = "";
	}
      }
else {
    $invalid_change = "";
}	
	if($invalid_change eq ''){
	        $unchanged++;
		#do nothing
		# print "$source_column==>unchanged\n";
	}
	else{
	        $changed++;
		$old = $source_column;
		@cells[$column_to_change] = $invalid_change;
		#print "$old==>changed to $source_column\n";
	}
#do this second to null all invalid_province values that are invalid according to FIMS and add them to locality
	if($INVALID{@cells[$column_to_change]}){
	        $added_to_locality++;
		$hold = @cells[$column_to_update];
		@cells[$column_to_update] = @cells[$column_to_change] . "; " . $hold;
		@cells[$column_to_change] = "";
		# print "$hold==>$Locality==>$source_column\n";
	      }
	print OUT join("\t",@cells) . "\n";
        #print OUT "$Main_Collector\t$Coll_Date\t$Coll_Num\t$Locality\t$source_column\t$Barcode_Number\t$County\t$Country\n";
        $linesout++;
      }

print 'rewrite pairs read:  ' . $rewritein . "\n";
print 'invalid names read:  ' . $invalidin . "\n";
print 'lines read:          ' . $linesin . "\n";
print 'lines output:        ' . $linesout . "\n";
print 'changed:             ' . $changed . "\n";
print 'unchanged:           ' . $unchanged . "\n";
print 'invalid added to locality: ' . $added_to_locality . "\n";



