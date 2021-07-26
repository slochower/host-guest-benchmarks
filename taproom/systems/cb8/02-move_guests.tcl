package require Orient
namespace import Orient::orient

set guests {"met"}
    #"esc"
    #"trd"
    #"pal"
    #"qui"
    #"gtr"
    #"thp"
    #"han"
    #"oan"
    #"dan"
    #"mpa"
    #"amm"
    #"met"
    #"fen"
    #"mor"
    #"hmo"
    #"ket"
    #"pcp"
    #"con"
#}
set total [llength $guests]

for {set i 0} {$i < $total} {incr i} {
	set guest_mol [lindex $guests $i]
	
	mol new $guest_mol/cb8-$guest_mol-p.pdb

	set host  [atomselect top "resname CB8 and nitrogen"]
	set guest [atomselect top "not resname CB8"]
    set all [atomselect top "all"]

    # Align whole system based on host
    $all moveby [vecinvert [measure center $host weight mass]]
    set I [draw principalaxes $host]
    set A [orient $host [lindex $I 2] {0 0 1}]
    $all move $A
    set I [draw principalaxes $host]
    set A [orient $host [lindex $I 1] {0 1 0}]
    $all move $A
    set I [draw principalaxes $host]
    $all move [transaxis y 90]

	$all writepdb $guest_mol/$guest_mol.pdb
	#file delete $guest_mol/$guest_mol.pdb
	
	$host delete
	$guest delete
	$all delete
	mol delete all
}
exit
