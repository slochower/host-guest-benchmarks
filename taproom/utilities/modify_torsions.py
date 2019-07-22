from openforcefield.typing.engines import smirnoff
from simtk import unit

force_field = smirnoff.ForceField('smirnoff99Frosst_experimental.offxml')

# t9
# [#1:1]-[#6X4:2]-[#6X4:3]-[#8X2:4]
# H1-C1-C2-O2
# GAFF v2.1
#   k = 0.16    per = 3
# SMIRNOFF99Frosst
#   k = 0.25    per = 1
#   k = 0.00    per = 3

#
# < Proper
# smirks = "[#1:1]-[#6X4:2]-[#6X4:3]-[#8X2:4]"
# id = "t9"
# idivf1 = "1"
# k1 = "0.000"
# periodicity1 = "3"
# phase1 = "0.0"
# phase2 = "0.0"
# k2 = "0.250"
# periodicity2 = "1"
# idivf2 = "1" / >

parameter = force_field.get_parameter_handler('ProperTorsions').parameters["[#1:1]-[#6X4:2]-[#6X4:3]-[#8X2:4]"]
assert(parameter.k[0] == 0.0 * unit.kilocalorie_per_mole)
assert(parameter.k[1] == 0.250 * unit.kilocalorie_per_mole)
assert(parameter.periodicity[0] == 3)
assert(parameter.periodicity[1] == 1)

parameter.k = [0.16 * unit.kilocalorie_per_mole]
parameter.periodicity = [3]
parameter.phase = [0 * unit.degrees]
parameter.idivf = [1]

# t87
# [#6X4:1]-[#6X4:2]-[#8X2H0:3]-[#6X4:4]
# C1-O1-C4-C3
# GAFF v2.1
#   k = 0.00    per = 1
#   k = 0.16    per = 2
#   k = 0.24    per = 3
# SMIRNOFF99Frosst
#   k = 0.10    per = 2
#   k = 0.38    per = 3

# < Proper
# smirks = "[#6X4:1]-[#6X4:2]-[#8X2H0:3]-[#6X4:4]"
# id = "t87"
# idivf1 = "1"
# k1 = "0.383"
# periodicity1 = "3"
# phase1 = "0.0"
# phase2 = "180.0"
# k2 = "0.100"
# periodicity2 = "2"
# idivf2 = "1" / >

parameter = force_field.get_parameter_handler('ProperTorsions').parameters["[#6X4:1]-[#6X4:2]-[#8X2H0:3]-[#6X4:4]"]

assert(parameter.k[0] == 0.383 * unit.kilocalorie_per_mole)
assert(parameter.k[1] == 0.100 * unit.kilocalorie_per_mole)
assert(parameter.periodicity[0] == 3)
assert(parameter.periodicity[1] == 2)

parameter.k = [0.16 * unit.kilocalorie_per_mole, 0.24 * unit.kilocalorie_per_mole]
parameter.periodicity = [2, 3]
parameter.phase = [0 * unit.degrees, 0 * unit.degrees]
parameter.idivf = [1, 1]

# t5
# O1-C4-C3-O3
# [#8X2:1]-[#6X4:2]-[#6X4:3]-[#8X2:4]
# GAFF v2.1
#   k = 0.02    per = 1
#   k = 0.00    per = 2
#   k = 1.01    per = 3
# SMIRNOFF99Frosst
#   k = 1.18    per = 2
#   k = 0.14    per = 3

# < Proper
# smirks = "[#8X2:1]-[#6X4:2]-[#6X4:3]-[#8X2:4]"
# id = "t5"
# idivf1 = "1"
# k1 = "0.144"
# periodicity1 = "3"
# phase1 = "0.0"
# phase2 = "0.0"
# k2 = "1.175"
# periodicity2 = "2"
# idivf2 = "1" / >

parameter = force_field.get_parameter_handler('ProperTorsions').parameters["[#8X2:1]-[#6X4:2]-[#6X4:3]-[#8X2:4]"]
assert(parameter.k[0] == 0.144 * unit.kilocalorie_per_mole)
assert(parameter.k[1] == 1.175 * unit.kilocalorie_per_mole)
assert(parameter.periodicity[0] == 3)
assert(parameter.periodicity[1] == 2)

parameter.k = [0.02 * unit.kilocalorie_per_mole, 1.01 * unit.kilocalorie_per_mole]
parameter.periodicity = [1, 3]
parameter.phase = [0 * unit.degrees, 0 * unit.degrees]
parameter.idivf = [1, 1]

force_field.to_file("smirnoff99Frosst-experimental-t5-t9-t87-modified.offxml")

force_field = smirnoff.ForceField("smirnoff99Frosst-experimental-t5-t9-t87-modified.offxml")
