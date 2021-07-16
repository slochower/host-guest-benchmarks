
set guests {"adm" "axm" "bhm" "c6m" "c7m" "c8m" "cha" "chm" "dpm" "haz" "hpm" "hxm" "phm" "prm"}
set total [llength $guests]

for {set i 0} {$i < $total} {incr i} {
	set guest_mol [lindex $guests $i]
	
	mol new $guest_mol/cb7-$guest_mol-p.pdb
}