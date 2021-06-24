#!/bin/bash -e

function get_packages {
    # First argument is an URL to a directory containing packages
    download_url="$1"

    # wget -nv -O - "$download_url"               -- Download HTML of package directory and send to stdout (-nv reduces verbosity)
    # | grep 'a href'                             -- Filter out lines that are not links (we're looking for links to rpms)
    # | sed -E -e 's:<a href="(.+[^\])".+:\1:'    -- Remove everything but the address part of links (these are already URL encoded)
    # | grep -v '/'                               -- '/' is invalid in RPM name but appears in links to different directories. Filter these out.
    # | xargs -I {} wget -nv "$download_url"/{}   -- Download the packages

    echo "-- Downloading packages from $download_url."
    SECONDS=0
    wget -nv -O - "$download_url" | grep 'a href' | sed -E -e 's:<a href="(.+[^\])".+:\1:' | grep -v '/' | xargs -P8 -I {} wget -nv "$download_url"/{}
    echo "-- Finished downloading packages from $download_url. Operation took $SECONDS seconds."
}

function make_tarball {
    archive_name=rpms.tar.gz

    for package_type in $packages_types; do
        mkdir -p RPMS/$package_type
        mv *.$package_type.rpm RPMS/$package_type/
    done

    mkdir -p RPMS/noarch
    mv *.noarch.rpm RPMS/noarch/

    echo "-- Packaging into a tarball..."
    tar --remove-files -czvf $archive_name RPMS
}

function help {
    echo "Package downloader. Downloads packages from a repository."
    echo "Usage:"
    echo '[MANDATORY] -d DIR -> space-separated list of directories in the RPM repository (passed with the -u) (e.g. "base update")'
    echo '[OPTIONAL]  -h -> print this help dialogue and exit'
    echo '[MANDATORY] -t TYPE -> select which type of packages to download. Can provide more than one type, separated by space. The valid types are: x86_64 aarch64 srpms'
    echo '[MANDATORY] -u URL -> URL to a root directory of a repository (e.g. https://packages.microsoft.com/cbl-mariner/1.0/prod/)'
    echo '[OPTIONAL]  -z -> create a tarball for each downloaded package type and clean up'
}

repository_url=
packages_types=
directories=
tar_packages=0

while getopts "d:ht:u:z" OPTIONS; do
    case ${OPTIONS} in
        d ) directories="$OPTARG" ;;
        h ) help; exit 0 ;;
        t ) packages_types="$OPTARG" ;;
        u ) repository_url=$OPTARG ;;
        z ) tar_packages=1 ;;
        ? ) echo -e "ERROR: INVALID OPTION.\n\n"; help; exit 1 ;;
    esac
done

if [[ -z "$directories" ]] || [[ -z "$packages_types" ]] || [[ -z "$repository_url" ]]; then
    echo -e "ERROR: Arguments '-d', '-t' and '-u' are mandatory!\n\n"
    help
    exit 2
fi

# Remove trailing directory separator, if any
if [[ $repository_url =~ ^.+/$ ]]; then
    echo "-- Removing trailing directory separator from $repository_url"
    repository_url=`echo $repository_url | head -c -2`
fi

# For benchmark purposes
before_run=$(date +%s)

# Iterate over directories and types, downloading the files
for directory in $directories; do
    echo "-- Downloading directory $directory..."
    for package_type in $packages_types; do
        echo "-- Downloading type $package_type for directory $directory..."

        # If these are not srpms, there is additional directory to skip
        appendix=
        if [[ ! "$package_type" == "srpms" ]]; then
            echo "-- Downloading RPMS - adding additional directory."
            appendix="/rpms"
        fi

        # Appendix contains the slash, if needed.
        get_packages "$repository_url"/"$directory"/"$package_type""$appendix"
    done
done

if [[ 1 == $tar_packages ]]; then
    make_tarball
fi

echo "Total execution time:"
after_run=$(date +%s)
date -d@$((before_run - now)) -u +%H:%M:%S
