package require Orient
namespace import Orient::orient

set guests {"adm" "axm" "bhm" "c6m" "c7m" "c8m" "cha" "chm" "dpm" "haz" "hpm" "hxm" "phm" "prm"}
set total [llength $guests]

for {set i 0} {$i < $total} {incr i} {
	set guest_mol [lindex $guests $i]
	
	mol new $guest_mol/cb7-$guest_mol-p.pdb

	set host  [atomselect top "resname CB7"]
	set guest [atomselect top "not resname CB7"]

	$guest moveby [vecinvert [measure center $guest]]
	set I [draw principalaxes $guest]
	set A [orient $guest [lindex $I 2] {0 0 1}]
	$guest move $A
	set I [draw principalaxes $guest]
	set A [orient $guest [lindex $I 1] {0 1 0}]
	$guest move $A
	set I [draw principalaxes $guest]
	
	set host_com [measure center $host]
	set guest_com [measure center $guest]
	$guest moveby [vecsub $host_com $guest_com]
	
	set all [atomselect top "all"]
	#$all set chain " "
	$all writepdb $guest_mol/$guest_mol.pdb
	#file delete $guest_mol/$guest_mol.pdb
	
	$host delete
	$guest delete
	$all delete
	mol delete all
}
exit
