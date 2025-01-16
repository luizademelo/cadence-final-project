# Formal Connectivity Verification

# Author(s):
# Luiza de Melo Gomes
#

# Parse the CSV connectivity specification defined in the $spec variable and
# generate assertions to verify that each connection in the CSV is proven in
# the RTL implementation

# Open the specification CSV file
set spec_file [open $spec r]


while {![eof $spec_file]} {
    set csv_line [gets $spec_file]
    
    
    set line_contents [split $csv_line ,]
    
    
    
    set source_signal [lindex $line_contents 3]
    set destination_signal [lindex $line_contents 5]
        
    
    assert "$source_signal == $destination_signal"
    
        
    
}

# Close the file after reading all lines
close $spec_file

