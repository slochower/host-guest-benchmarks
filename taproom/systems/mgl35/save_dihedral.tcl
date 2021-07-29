
set f [open "dihedrals.dat" w]

foreach dihedral [label list Dihedrals] {
  # Dihedral atom indices
  set i1 [lindex [split [lindex $dihedral 0]] 1]
  set i2 [lindex [split [lindex $dihedral 1]] 1]
  set i3 [lindex [split [lindex $dihedral 2]] 1]
  set i4 [lindex [split [lindex $dihedral 3]] 1]
  
  # Dihedral atom names
  set a1 [[atomselect top "index $i1"] get name]
  set a2 [[atomselect top "index $i2"] get name]
  set a3 [[atomselect top "index $i3"] get name]
  set a4 [[atomselect top "index $i4"] get name]
  
  # Dihedral atom resid
  set r1 [[atomselect top "index $i1"] get resid]
  set r2 [[atomselect top "index $i2"] get resid]
  set r3 [[atomselect top "index $i3"] get resid]
  set r4 [[atomselect top "index $i4"] get resid]
  
  # Dihedral
  set dih [lindex $dihedral 4]
  
  # Print
  puts $f ":${r1}@${a1} :${r2}@${a2} :${r3}@${a3} :${r4}@${a4} $dih"
}

close $f