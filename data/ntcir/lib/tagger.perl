#!/usr/bin/perl

#
# uspto_tag.prl: Inserting NTCIR tags in USPTO patent data
# by Atsushi Fujii <ntcadm-patent@nii.ac.jp>
#
# 2003.09.10: ver 1.0
#
# Usage: uspto_tag.prl <file(s)>
# file(s): plain text or gzipped form
#

$| = 1;

# Description of NTCIR tags
@tag = (
	'APP-NO',	# Application number
	'APP-DATE',	# Application date
	'PUB-NO',	# Publication number
	'PUB-TYPE',	# Publication type
	'PUB-DATE',	# Publication date (dummy)
	'PAT-NO',	# Patent number
	'PAT-TYPE',	# Patent type
	'PUB-DATE',	# Publication date
	'PRI-IPC',	# Primary IPC
	'IPC-VER',	# IPC version
	'PRI-USPC',	# Primary USPC
	'PRIORITY',	# Priority information
	'CITATION',	# Citation(s)
	'INVENTOR',	# Inventor(s)
	'ASSIGNEE',	# Assignee(s)
	'TITLE',	# Title
	'ABST',		# Abstract
	'SPEC',		# Specification
	'CLAIM',	# Claim(s)
	);

$n_field = @tag;

foreach $file (@ARGV) {
    if ($file =~ /\.gz$/) {
	open(IN, "zcat $file |") || die "$file: $!";
    } else {
	open(IN, $file) || die "$file: $!";
    }
    $line = 1;
    while ($cont = <IN>) {
	chomp($cont);
	@buf = split(/\t/, $cont);
	$line++;

	&tagging(\@buf);

    }
    close(IN);

    $line--;
    # print STDERR "file = $file: #records = $line\n";
}

sub tagging (\@) {
    my($ref_cont) = @_;
    my(@buf);

    $claim = pop(@$ref_cont);

    $patno = $$ref_cont[5];	# Patent number
    if (length($patno) == 7) {
	$patno = '0' . $patno;
    }
    $pubdate = $$ref_cont[7];	# Publication date
    ($year) = ($pubdate =~ /^([0-9]{4})/);
    $docno = 'PATENT-US-GRT-' . $year . '-' . $patno;
    
    $$ref_cont[11] =~ s/<tab>/\t/g;
    @citation = split(/<tab>/, $$ref_cont[12]);
    @buf = ();
    while (@citation) {
	$citation = shift(@citation);
	$date = shift(@citation);
	$citation .= '/' . $date;
	push(@buf, $citation);
    }
    $$ref_cont[12] = join("\t", @buf);

    print "<DOC>";
    print "<DOCNO>$docno</DOCNO>";
    $i = 0;
    while ($i < 17) {
	$field = shift(@$ref_cont);
	if ($field ne '\N') {
	    print "<$tag[$i]>$field</$tag[$i]>";
	}
	$i++;
    }
    $spec = join("\t", @$ref_cont);
    print "<SPEC>$spec</SPEC>";
    print "<CLAIM>$claim</CLAIM>";
    print "</DOC>\n";
}
