set spec_file [open "direct.csv" r]

while {![eof $spec_file]} {
    set csv_line [gets $spec_file]
    
    # Split the CSV line into individual fields
    set line_contents [split $csv_line ,]
    
    # Check if the second index is not empty
    if {[string length [lindex $line_contents 2]] > 0} {
        # Concatenate the second and third indices
        set concatenated [format "%s%s" [lindex $line_contents 2] [lindex $line_contents 3]]
        puts "Concatenated value: $concatenated"
    }
    
    # Extract source and destination signals (optional)
    set source_signal [lindex $line_contents 3]
    set destination_signal [lindex $line_contents 5]
}

# Close the file after reading all lines
close $spec_file
