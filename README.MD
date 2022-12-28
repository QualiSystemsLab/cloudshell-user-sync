[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python/)
[![Lint and Test](https://github.com/QualiSystemsLab/cloudshell-user-sync/actions/workflows/lint-test.yml/badge.svg)](https://github.com/QualiSystemsLab/cloudshell-user-sync/actions/workflows/lint-test.yml)
[![PyPI version](https://badge.fury.io/py/cloudshell-user-sync.svg)](https://badge.fury.io/py/cloudshell-user-sync)

# cloudshell-user-sync

A CLI tool to Sync LDAP / Active Directory Groups with Cloudshell groups.
This package will pull LDAP data, compare state of cloudshell group, and add/remove users to sync the groups.

### Important Notes 

- This package does NOT import/create users from LDAP - only syncs already imported users across groups.
  - Users are NOT deleted from system during sync - only add/remove to group action performed.
  - Users must be first [manually imported](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/AD-Imprt-Usrs-frm-AD-grp-file.htm) or [auto-imported on login](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/AD-Intg-Auto-Imprt.htm?tocpath=CloudShell%20Administration%7CCloudShell%20Identity%20Management%7CAccess%20Control%20and%20Authentication%7CActive%20Directory%20Integration%7C_____1) to a default group.
- Non-imported cloudshell users will NOT be evicted from a synced group.
  - This tool only aims to manage the imported ldap users.
  - Groups can be hybrid with "regular" users. 
- This tool can be configured to manage only a subset of cloudshell groups.
- If possible, to improve performance of LDAP search, place target ldap users together under common root  in LDAP Tree.
  - This will allow to set a lower base root DN [(distinguished name)](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ldap/distinguished-names) to allow quicker ldap searches.
  - Note that LDAP groups and users are not necessarily in same location of ldap tree


### Installation
```commandline
pip install cloudshell-user-sync
```

### Commands
```commandline
Commands:
  config        View or Set Config - Pass no params to view config
  credential    Set Credentials For Cloudshell and LDAP
  mapping       Set LDAP group --> Cloudshell Groups Mapping
  run           Pull LDAP Data and sync to Cloudshell
  runscheduler  Run sync on infinite scheduler
  service       Install Windows service to run job automatically
  version       Display CLI version
 
```
### Basic Usage
1. configure credentials (stored in OS specific credential manager)
2. set config values for target cloudshell server
3. Set config values for target LDAP server
4. set LDAP -> Cloudshell Group Mappings
5. Do manual sync run to test 
6. Configure service to run job automatically

#### Configure Credentials
Set Cloudshell Credential
```commandline
usersync credential admin admin --target cloudshell
```
Set LDAP Credential
```commandline
usersync credential CN=Administrator,CN=Users,DC=samplecorp,DC=example,DC=com LDAP_DN_Password --target ldap
```
- User is the full distinguished name (DN) as seen in AD explorer 


#### Set Config Values
Credentials must be set through CLI to be stored in credential manager. 
The other values can be set directly in file or optionally in CLI

Default Config Path:
- Windows: C:\ProgramData\QualiSystems\CloudshellUserSync\ldap_config.json
- Linux: /opt/CloudshellUserSync/ldap_config.json

view current config state
```commandline
usersync config
```

CLI Set config actions follows the pattern:
```
usersync config <target> <key> <value>
```

Set cloudshell server details
```commandline
usersync config cloudshell server localhost
```

Set ldap details
```commandline
usersync config ldap server 10.0.0.7
usersync config ldap base_dn DC=samplecorp,DC=example,DC=com
```
- base_dn is where the ldap search will start from
- Filter scheme used is: `(&(objectClass=user)(memberOf=<GROUP_DN>))`

#### Set LDAP mappings
Can map one LDAP source group to multiple cloudshell groups (ie a list)

View only mapping config:
```commandline
usersync mapping
```

Set mapping follows pattern:
```commandline
usersync mapping <LDAP_GROUP_DN> --csgroups <CSGROUP1>,<CSGROUP2>,<CSGROUP3>
```

sample:
```commandline
usersync mapping CN=nattigroup,DC=natticorp,DC=example,DC=com --csgroups <CSGROUP1>,<CSGROUP2>,<CSGROUP3>
```

### Configure Windows Service
Install and run job as managed windows service.

Install service
```commandline
usersync service install
```

Start Service
```commandline
usersync service start
```

Notes:
- After installation, must set service to run as same Logon user that ran install
  - This is so service can access windows credential manager with same user that set the credentials
- Set startup type to auto
- Check log to ensure no errors are occuring. 
- Set log level to debug to see more details on users found per LDAP request 


### Linux Service
No linux service generation command included. The following options are possible.
- Schedule the "run" command to a cron job
- Wrap the "runscheduler" command into a systemd service

### Logs
Both manual runs and scheduled runs log to the same rotating log file.

- Windows:
`C:\ProgramData\QualiSystems\CloudshellUserSync\Logs\UserSync.log`
- Linux:
`/opt/CloudshellUserSync/Logs/UserSync.log`

### Dependencies
- [LDAP3](https://github.com/cannatag/ldap3) for pulling source LDAP/AD data
- [Schedule](https://github.com/dbader/schedule) as cross-platform cron-like scheduler
- [Keyring](https://github.com/philipn/python-keyring-lib) to store credentials in OS
- [Pywin32](https://github.com/mhammond/pywin32) - windows service installer
- `cloudshell-automation-api` to update cloudshell groups

### License

Free Software: MIT License