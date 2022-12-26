[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python/)
[![Lint and Test](https://github.com/QualiSystemsLab/cloudshell-user-sync/actions/workflows/lint-test.yml/badge.svg)](https://github.com/QualiSystemsLab/cloudshell-user-sync/actions/workflows/lint-test.yml)
[![PyPI version](https://badge.fury.io/py/cloudshell-user-sync.svg)](https://badge.fury.io/py/cloudshell-user-sync)

# cloudshell-user-sync

A CLI tool to Sync LDAP / Active Directory Groups with Cloudshell groups.
This package will pull LDAP data, compare state of cloudshell group, and add/remove users to sync the groups.

### Important Notes 

- This package does NOT import users from LDAP. Only Syncs already imported Users
  - Users must be first [manually imported](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/AD-Imprt-Usrs-frm-AD-grp-file.htm) or [auto-imported on login](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/AD-Intg-Auto-Imprt.htm?tocpath=CloudShell%20Administration%7CCloudShell%20Identity%20Management%7CAccess%20Control%20and%20Authentication%7CActive%20Directory%20Integration%7C_____1) 
- Non-imported users added to a cloudshell group that don't exist in LDAP will be removed from that cloudshell group.
  - This tool expects to fully manage the configured cloudshell groups. 
  - This tool can be configured to manage only a subset of cloudshell groups


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

Set cloudshell server sample
```commandline
usersync config cloudshell server localhost
```
Set ldap server sample
```commandline
usersync config ldap server 10.0.0.7
```

#### Set LDAP mappings
Can map one LDAP source group to multiple cloudshell groups (ie a list)

View only mapping config:
```commandline
usersync mapping
```

Set mapping follows pattern:
```commandline
usersync mapping <LDAP_GROUP> --csgroups <CSGROUP1>,<CSGROUP2>,<CSGROUP3>
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
  - This is so it can access windows credential manager.
- Set startup type to auto if desired
- Check log to ensure no errors are occuring. 
  - The service will not crash on errors due to lost connectivity to target servers. 


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