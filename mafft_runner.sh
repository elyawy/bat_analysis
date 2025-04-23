#!/bin/bash

# Check if directory path is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Store the parent directory path
PARENT_DIR="$1"

# Check if the provided path is a directory
if [ ! -d "$PARENT_DIR" ]; then
    echo "Error: '$PARENT_DIR' is not a directory"
    exit 1
fi

echo "Processing subdirectories in: $PARENT_DIR"

# Find all directories that are exactly one level deep
for DIR in "$PARENT_DIR"/*/; do
    if [ -d "$DIR" ]; then
        echo "Processing directory: $DIR"
        
        # Change to the subdirectory
        cd "$DIR" || continue
        
        # Check if msa.fasta exists in this directory
        if [ ! -f "msa.fasta" ]; then
            echo "  No msa.fasta file found in $DIR"
            cd - > /dev/null
            continue
        fi
        
        echo "  Running MAFFT on msa.fasta"
        
        # Run MAFFT command
        mafft --retree 2 msa.fasta > realigned.fasta
        
        if [ $? -eq 0 ]; then
            echo "  Successfully created realigned.fasta"
        else
            echo "  Error running MAFFT on msa.fasta"
        fi
        
        # Return to parent directory
        cd - > /dev/null
    fi
done

echo "Processing complete!"