#!/bin/bash

echo "==============================================="
echo "QUICK CHAPTER STATUS CHECK"
echo "==============================================="
echo

for i in {1..14}; do
    bab=$(printf "Bab-%02d-*" $i)
    if ls -d $bab 2>/dev/null | grep -q .; then
        dir=$(ls -d $bab | head -1)
        prog_count=$(ls "$dir/praktikum"/*.py 2>/dev/null | grep -E "^[0-9]" | wc -l)
        if [ $prog_count -gt 0 ]; then
            echo "✓ $dir: $prog_count programs"
        else
            echo "✗ $dir: No programs found"
        fi
    fi
done
