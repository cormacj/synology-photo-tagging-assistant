#!/bin/env bash
# Make the webpages for the list of Synology tags
# (c) Cormac McGaughey, 2025

# Create a temp file for data storage
tmpfile=`mktemp`

# Find the path of this script. This will allow me to enforce the path and be a bit more secure about the next commands
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Load the configuration variables.
source $SCRIPT_DIR/configs.sh

# First, grab a list of ids and names from the shared database space where a tag is actually in use. Sort it by name.
# A note here: Synology will store old tags, eg if you typoed a tag and then corrected it, the typo hangs around the database,
# so if I didn't specify count>0 you would see all the old unused tags.
#
sudo psql -U postgres -A -t -d synofoto -c "select id,name from public.general_tag where id_user=0 and count>0 order by name_for_sort;" >$tmpfile

# Call the python script to covert the query output into a usable PHP file.
python3 $SCRIPT_DIR/make_tags_directory.py $tmpfile $WEB_FILES_LOCATION/index.php $URL

# Second, a more complex query to pull a list of files that have no tags. This also returns, the internal ID, folder name, and filename.
#
sudo psql -U postgres -A -t -d synofoto -c "select date(to_timestamp(takentime)) as d,unit.id,folder.name,filename from unit,folder where id_folder=folder.id and unit.id_user=0 and not exists (select null from many_unit_has_many_general_tag where id_unit=unit.id) order by d desc,unit.id;" >$tmpfile

# Call a script to convert that query result into a .html file.
python3 $SCRIPT_DIR/untagged_year.py $tmpfile $WEB_FILES_LOCATION/untagged_photos.html $URL >/dev/null

# Finally, clean up.
rm $tmpfile
