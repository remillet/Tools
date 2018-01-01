$runtype = @ARGV[0];
$location_column = 0 + @ARGV[1];
$crate_column = 0 + @ARGV[2];
while (<STDIN>) {
    chomp;
    s/\r//;
    @cell = split "\t",$_,-1;
    # BAMPFA-412
    # "Asian Study"* => "located in Asian Study Center"
    # "Study Center*" => "located in Art Study Centers"
    # Ditto for "Gallery*", "Reading Room*", "Community Gallery*" = "On view"
    # Everything else is "Not on view"
    #
    # ok, ok, yes there is an implied if-then-else hidden here...I think it's fine, at least for now.
    $location = $cell[$location_column];
    $status = "Not on view";
    $status = "On View" if $location =~ /Gallery/i;
    $status = "On View" if $location =~ /Oxford, Lobby/i;
    $status = "located in Asian Study Center" if $location =~ /Asian Study/i;
    $status = "located in Art Study Center" if $location =~ /^Study\b/i;
    $i++;
    if ($i == 1) {
        $status = "status";
    }
    else {
        if ($runtype eq 'public') {
            $cell[$crate_column] = '-REDACTED-';
            $cell[$location_column] = '-REDACTED-';
        }
    }
    $_ = join("\t",@cell);
    # add to tail end of record.
    s/$/\t$status\n/;
    print;
}
