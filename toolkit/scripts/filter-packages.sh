#!/bin/bash -e

function filter_packages {
    # First argument is a path to the packages directory
    rpms_directory="$1"

    # Used later
    fields_cutoff=2
    if [[ $ignore_versions -eq 1 ]]; then
        fields_cutoff=3
    fi

    duplicates_list=$(find "$rpms_directory" -name '*.rpm' -exec basename {} \; | # Find all the rpms leaving only file names
                          sort -V |                                               # Sort to stack duplicates together. Sort like version numbers (-V)
                          rev |                                                   # Read backwards to inverse the order of the fields
                          cut -d'-' -f ${fields_cutoff}- |                        # Separate into fields by '-' skipping the first two (in case of ignore_versions - 3)
                                                                                  # (actually last - we're inversed) fields (filters out release and extension)
                                                                                  # in case of -i being passed, ignore versions as well.
                          rev |                                                   # Return to normal order
                          uniq -d |                                               # Print only duplicates
                          awk '{print}' ORS=' ')                                  # Join lines with space instead of newline

    remove_function="rm -v"
    if [[ $pretend -eq 1 ]]; then
        remove_function="echo Would remove: "
    fi

    for duplicate in $duplicates_list; do
        echo "Processing package '$duplicate'."
        name_search="${duplicate}-[0-9]*"

        # and remove them (explicitly list removed items)
        packages_to_remove=$(find "$rpms_directory" -name "$name_search" |# Find all the RPM files with the same name (different versions treated as different names without -i)
                                 sort -V -r | # Read backwards and sort a version numbers (-V) and print in reverse(-r) to have the latest version at the top.
                                 tail -n +2) # After the sort, the first path is of the latest version. Get a list of all the other RPMs (duplicates), starting line 2.

        for package in $packages_to_remove; do
            $remove_function "$package"
        done

        # Run a more advanced query again to work correctly when doing a -p run
        echo "Left:" $(find "$rpms_directory" -name "$name_search" | sort -V -r | awk '{print}' ORS=' ' | cut -d' ' -f1 )
        echo #newline
    done
}

function help {
    echo "Package filter. Filter out (remove) duplicate packages."
    echo "Usage:"
    echo '[MANDATORY] -d DIR -> path to the directory which contains RPMS (this will) affect all subdirectories'
    echo '[OPTIONAL]  -h     -> print this help dialogue and exit'
    echo '[OPTIONAL]  -i     -> ignore version numbers when looking for the duplicates.'
    echo '[OPTIONAL]  -p     -> pretend mode - just print the packages without removing them'
}

directory=
pretend=0
ignore_versions=0

while getopts "d:hpi" OPTIONS; do
    case ${OPTIONS} in
        d ) directory="$OPTARG" ;;
        h ) help; exit 0 ;;
        i ) ignore_versions=1 ;;
        p ) pretend=1 ;;
        ? ) echo -e "ERROR: INVALID OPTION.\n\n"; help; exit 1 ;;
    esac
done

if [[ -z "$directory" ]]; then
    echo -e "ERROR: Argument '-d' is mandatory!\n\n"
    help
    exit 2
fi

filter_packages "$directory"
