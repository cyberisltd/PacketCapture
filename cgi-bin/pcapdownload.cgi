#!/usr/bin/perl -w

#VERSION 0.2 - 2/11/2011
#Author Geoff Jones nop@0x90.co.uk

use CGI; # load CGI routines
use CGI::Carp qw (fatalsToBrowser);
use Safe;
use strict;
use File::Find;

my $pcapdir = "/data/pcap/";
my $pcapext = "pcap";

my $query = CGI->new; # create new CGI object

my $filter = $query->param('bpffilter') || "";
my $starttime = $query->param('starttime');
my $endtime = $query->param('endtime');
my $sensor = $query->param('sensor');

my ($syear, $smonth, $sday, $shour, $smin, $ssec) = &checktime($starttime);
my ($eyear, $emonth, $eday, $ehour, $emin, $esec) = &checktime($endtime);

find(\&wanted, $pcapdir);

my @files;

sub wanted {
	/^[0-9]{12}-$sensor\.$pcapext/s &&
	push (@files, $File::Find::name);
}

@files = sort @files;

my ($startfile, $endfile);

#Check filter
die "Invalid filter '$filter'" if ($filter =~ /^[^a-z0-9 ]*$/i);


# Loop through all the possible files to chose from (this could be many thousand).
for (my $i=0; $i < @files; $i++ ) {

	# Pull out the timestamp
	$files[$i] =~ m#/([0-9]{12}).*\.$pcapext#i;
	my $filedate = $1."00";
 
	if ($starttime < $filedate && !defined $startfile) {	
		$startfile = $i;

		my $packettime;
		#Find the first file in the time window
		do {
			$startfile = $startfile - 1;
			my $output = `/usr/sbin/tcpdump -r $files[$startfile] -c 1 -n -tttt`;
			$output =~ /([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})/;
			$packettime = $1;
			$packettime =~ s/[\:\-\.\ ]//g;
		} while ($starttime < $packettime);		
		
		#Now starting with the next file, loop through until you find the end...
		$endfile = $startfile ;
		do {
			$endfile++;
			my $output = `/usr/sbin/tcpdump -r $files[$endfile] -c 1 -n -tttt`;
			$output =~ /([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})/;
			$packettime = $1;
			$packettime =~ s/[\:\-\ ]//g;
		} while ($endtime > $packettime);
	}
}

die "No file(s) present the date range specified\n" unless (defined $startfile && defined $endfile);
@files = @files[$startfile..$endfile];

system("/usr/bin/mergecap -w - @files | /usr/sbin/tcpdump -r - -w /tmp/$$.$pcapext $filter");
system("/usr/bin/editcap -A '$syear-$smonth-$sday $shour:$smin:$ssec' -B '$eyear-$emonth-$eday $ehour:$emin:$esec' /tmp/$$.$pcapext /tmp/$$.$pcapext.filtered");

die "File /tmp/$$.$pcapext does not exist" unless (-e "/tmp/$$.$pcapext");
die "Zero bytes in filtered file\n" unless (-s "/tmp/$$.$pcapext.filtered");
die "File size larger that 500MB" unless (-s "/tmp/$$.$pcapext.filtered" < 524288000);

print $query->header(-type=>'application/pcap',-attachment=>"$starttime-$endtime.$pcapext");

open (FILTERED, "< /tmp/$$.$pcapext.filtered") or die "Cannot read filtered pcap\n";

while (<FILTERED>) {
	print;
}

sub checktime() {
	my $time = shift;
	if ($time =~ /([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})/) {
		my $year = $1;
		my $month = $2;
		my $day = $3;
		my $hour = $4;
		my $min = $5;
		my $sec = $6;
		
		die "Invalid date/time\n" if $sec > 59 || $min > 59 || $hour > 23 || $day > 31 
			|| $month > 12;

		return ($year, $month, $day, $hour, $min, $sec);
	}
	else { die "Invalid date format\n" };
}

END {
	unlink "/tmp/$$.$pcapext.filtered" if (-e "/tmp/$$.$pcapext.filtered");
	unlink "/tmp/$$.$pcapext" if (-e "/tmp/$$.$pcapext");
}
