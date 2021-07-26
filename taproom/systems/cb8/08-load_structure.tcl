
set guests {
    "esc"
    "trd"
    "pal"
    "qui"
    "gtr"
    "thp"
    "han"
    "oan"
    "dan"
    "mpa"
    "amm"
    "met"
    "fen"
    "mor"
    "hmo"
    "ket"
    "pcp"
    "con"
}
set total [llength $guests]

for {set i 0} {$i < $total} {incr i} {
	set guest_mol [lindex $guests $i]
	
	mol new $guest_mol/cb8-$guest_mol-p.pdb
	#mol new $guest_mol/$guest_mol.pdb
	#mol new $guest_mol/$guest_mol-aligned-z.pdb
}
