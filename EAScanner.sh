#!/bin/bash
#Extracts occurances of a file path from the output of a 
echo "Please make sure to run script from same Original_file PATH"
read -p "Enter filename: " original_file
cp $original_file tempfile.txt && sed 's/ /\n/g' tempfile.txt > tempfile1.txt && sed -i '.bak' '/^$/d' tempfile1.txt  && cat tempfile1.txt | grep '^/' | sort |uniq -c | sort -k2nr |sort -r| awk '{printf("%s,%s\n",$1,$2)}' > filtered-sorted-file.txt && rm -rf tempfile*.txt
