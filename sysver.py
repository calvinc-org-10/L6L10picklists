_appname='L6 to L10 sales/picking'
_base_ver_major=1
_base_ver_minor=0
_base_ver_patch=0
_ver_date='2026-04-09'
_base_ver = f'{_base_ver_major}.{_base_ver_minor}.{_base_ver_patch}'
# _base_ver = '2026.04.09.0000' # use date-based versioning for now - easier to track with changelog and avoids issues with updating version for each commit during development
sysver = {
    'DEV': f'DEV{_base_ver}', 
    'PROD': _base_ver,
    'DEMO': f'DEMO{_base_ver}'
    } 

# Changelog:
# Version - Date - Description
# 1.0.0 - Initial working version with basic functionality to view and edit picklists, and view related sales orders. Still a lot of work to do, but this is a good stopping point for the initial version. Next steps will be to add functionality to create new picklists, and to link to related records like sales orders and inventory items. Also need to do more testing and bug fixing, and add some error handling and input validation.

