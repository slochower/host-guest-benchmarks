
set f [open "bonds.dat" w]

foreach bond [label list Bonds] {
  # Bond atom indices
  set i1 [lindex [split [lindex $bond 0]] 1]
  set i2 [lindex [split [lindex $bond 1]] 1]
  
  # Bond atom names
  set a1 [[atomselect top "index $i1"] get name]
  set a2 [[atomselect top "index $i2"] get name]
  
  # Bond atom resid
  set r1 [[atomselect top "index $i1"] get resid]
  set r2 [[atomselect top "index $i2"] get resid]
  
  # Bond
  set dist [lindex $bond 2]
  
  # Print
  puts $f ":${r1}@${a1} G1 $dist"
}

close $f
