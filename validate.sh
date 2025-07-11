#!/usr/bin/env bash
#
# A file to validate the install
#
# (c) Cormac McGaughey, 2025

# If something fails, print a useful message
function fail {
    printf '%s\n' "$1" >&2 ## Send message to stderr.
    exit "${2-1}" ## Return a code specified by $2, or 1 by default.
}

# Can we make a temp file?
tmpfile=`mktemp`

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Can we read the config properly?
source $SCRIPT_DIR/configs.sh || fail "Error in configs.sh"

# Can we write to the webserver folder?
touch $WEB_FILES_LOCATION/validate.txt || fail "Error writing to web files location"

# Can we query the database correctly?
sudo psql -U postgres -A -t -d synofoto -c "select id,name from public.general_tag where id_user=0 and count>0 order by name_for_sort limit 1;" > $WEB_FILES_LOCATION/validate.txt || fail "Error running psql (check sudoers.d)"

# Cleanup our temp files
rm $WEB_FILES_LOCATION/validate.txt
rm $tmpfile

echo "Everything worked!"
