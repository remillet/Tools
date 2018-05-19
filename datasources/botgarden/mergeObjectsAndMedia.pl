use strict;

my %count ;
my $delim = "\t";
my $runtype = $ARGV[2]; # generate media for public or internal


open MEDIA,$ARGV[0] || die "couldn't open media file $ARGV[0]";
my %media ;
while (<MEDIA>) {
  $count{'media'}++;
  chomp;
  s/\r//g;
  my ($objectcsid, $objectnumber, $mediacsid, $description, $filename, $creatorrefname, $creator, $blobcsid, $copyrightstatement, $identificationnumber, $rightsholderrefname, $rightsholder, $contributor, $imageNumber, $approvedforweb) = split /$delim/;
  #print "$blobcsid $objectcsid\n";
  # eliminate non-public images from public portal
  next if ($approvedforweb eq 'no') && ($runtype eq 'public');
  $media{$objectcsid} .= $blobcsid . ',';
}

open METADATA,$ARGV[1] || die "couldn't open metadata file $ARGV[1]";
while (<METADATA>) {
  $count{'metadata'}++;
  chomp;
  s/\r//g;
  my ($id, $objectid, @rest) = split /$delim/;
  # botgarden is special here: csid got buried in the record...
  $objectid = $rest[39];
  # insert list of blobs as final column
  my $mediablobs = $media{$objectid};
  if ($mediablobs) {
    $count{'matched'}++;
  }
  else {
    $count{'unmatched'}++;
  }
  $mediablobs =~ s/,$//; # get rid of trailing comma
  print $_ . $delim . $mediablobs . "\n";
}

foreach my $s (sort keys %count) {
 warn $s . ": " . $count{$s} . "\n";
}
