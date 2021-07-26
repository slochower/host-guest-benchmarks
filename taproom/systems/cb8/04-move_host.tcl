set guests {"met"}
#    "esc"
#    "trd"
#    "pal"
#    "qui"
#    "gtr"
#    "thp"
#    "han"
#    "oan"
#    "dan"
#    "mpa"
#    "amm"
#    "met"
#    "fen"
#    "mor"
#    "hmo"
#    "ket"
#    "pcp"
#    "con"
#}

set total [llength $guests]

for {set i 0} {$i < $total} {incr i} {
	set guest_mol [lindex $guests $i]
	
	mol new $guest_mol/$guest_mol-aligned.pdb

	set host  [atomselect top "resname CB8 and nitrogen"]
	set guest [atomselect top "not resname CB8"]
    set all [atomselect top "all"]

    # Align whole system based on host
	set vec [vecsub [measure center $host] [measure center $guest]]
	#$guest moveby "0 0 [lindex $vec 2]"
	$guest moveby $vec
	#$guest moveby {0 0 2}

	$all writepdb $guest_mol/$guest_mol-aligned-z.pdb
	
	$host delete
	$guest delete
	$all delete
	mol delete all
}
exit
