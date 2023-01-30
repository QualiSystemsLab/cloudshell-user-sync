[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python/)
[![Lint and Test](https://github.com/QualiSystemsLab/cloudshell-user-sync/actions/workflows/lint-test.yml/badge.svg)](https://github.com/QualiSystemsLab/cloudshell-user-sync/actions/workflows/lint-test.yml)
[![PyPI version](https://badge.fury.io/py/cloudshell-user-sync.svg)](https://badge.fury.io/py/cloudshell-user-sync)

# cloudshell-user-sync

A CLI tool to Sync LDAP / Active Directory Groups with Cloudshell groups.
This package will pull LDAP data, compare state of cloudshell group, and add/remove users to sync the groups.

Sync job can be run as scheduled cron job, windows task, or wrapped into linux / windows service.

### Important Notes

- This package does NOT import/create users from LDAP - only syncs already imported users across groups.
    - Users are NOT deleted from system during sync - only add/remove to group action performed.
    - Users must be
      first [manually imported](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/AD-Imprt-Usrs-frm-AD-grp-file.htm)
      or [auto-imported on login](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/AD-Intg-Auto-Imprt.htm?tocpath=CloudShell%20Administration%7CCloudShell%20Identity%20Management%7CAccess%20Control%20and%20Authentication%7CActive%20Directory%20Integration%7C_____1)
      to a default group.
- Non-imported cloudshell users will NOT be evicted from a synced group.
    - This tool only aims to manage the imported ldap users.
    - Groups can be hybrid with "regular" users.
- This tool can be configured to manage only a subset of cloudshell groups.
- If possible, to improve performance of LDAP search, place target ldap users together under common root in LDAP Tree.
    - This will allow to set a lower base
      root [Distinguished Name](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ldap/distinguished-names)
      to allow quicker ldap searches.
    - Note that LDAP groups and users are not necessarily in same location of ldap tree. The Base DN must be where the
      users are not the groups.

### Installation

Install with pip or download from Github releases

```commandline
pip install cloudshell-user-sync
```

Recommended to install into dedicated [venv](https://docs.python.org/3/library/venv.html)

```commandline
mkdir user-sync-venv
cd user-sync-venv
venv .
cd Scripts
activate
pip install cloudshell-user-sync
```

### Commands

```commandline
Commands:
  config      View or Set Config - Pass no params to view config
  credential  Set Credentials For Cloudshell and LDAP           
  mapping     Set LDAP group --> Cloudshell Groups Mapping      
  run         Pull LDAP Data and sync to Cloudshell
  version     Display CLI version
```

### Basic Usage

1. Configure venv and install package
2. configure credentials (stored in OS specific credential manager)
3. set config values for target cloudshell server
4. Set config values for target LDAP server
5. set LDAP -> Cloudshell Group Mappings
6. Do manual sync run to test
7. Configure scheduled task to run automatically

#### Configure Credentials

Set Cloudshell Credential

```commandline
usersync credential admin admin --target cloudshell
```

Set LDAP Credential

```commandline
usersync credential CN=Administrator,CN=Users,DC=samplecorp,DC=example,DC=com LDAP_DN_Password --target ldap
```

- LDAP User is the
  full [Distinguished Name](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ldap/distinguished-names)
- To find DN can use [AD Explorer](https://learn.microsoft.com/en-us/sysinternals/downloads/adexplorer)
  or [LDAP Explorer](https://ldaptool.sourceforge.net/)

#### Set Config Values

Credentials must be set through CLI to be stored in credential manager.
The other values can be set directly in file or optionally in CLI

Default Config Path:

- Windows: C:\ProgramData\QualiSystems\CloudshellUserSync\ldap_config.json
- Linux: /opt/CloudshellUserSync/ldap_config.json

View current config state by running `usersync config`:

```json
{
  "service_config": {
    "job_frequency_seconds": 30,
    "log_level": "DEBUG"
  },
  "cloudshell_details": {
    "user": "admin",
    "password": "************",
    "server": "192.168.85.114",
    "domain": "Global"
  },
  "ldap_details": {
    "user_dn": "CN=Administrator,CN=Users,DC=testcorp,DC=example,DC=com",
    "password": "************",
    "server": "192.168.85.115",
    "base_dn": "DC=testcorp,DC=example,DC=com"
  },
  "ldap_mappings": [
    {
      "ldap_dn": "CN=testgroup,DC=testcorp,DC=example,DC=com",
      "cloudshell_groups": [
        "QA"
      ]
    }
  ]
}
```

CLI Set config actions follows the pattern:

```
usersync config <target> <key> <value>
```

Set cloudshell server details:

```commandline
usersync config cloudshell server localhost
```

Set LDAP details:

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

### Configure Scheduled Task

To set command to run automatically with OS level scheduler.

- Get path to "usersync.exe" executable installed in venv and schedule the `run` command
- Set logon for task with same user that set credentials with `usersync credential` command

```commandline
path-to-usersync.exe run
```

#### Windows Scheduled Task

Configure Task Scheduler according
to [article](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10)

#### Linux Cron Job

Configure according to [article](https://www.freecodecamp.org/news/cron-jobs-in-linux/)

### Service creation

Run scheduler uses the schedule module to run job infinitely at configured frequency.

- Set the job frequency seconds in config
- set credentials via cli `usersync credential`
- configure the `runscheduler` command into [nssm](https://nssm.cc/)
  or [systemd](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- Set service logon as same user that configured the credentials (requirement for keyring module to work properly)
- Alternatively, for windows, see the python [util install](util/windows_service.py) script option
- usersync.exe will be installed inside python/Scripts of python environment

Runscheduler command (give full path to exe)

```commandline
usersync.exe runscheduler
```

### Logs

Both manual runs and scheduled runs log to the same rotating log file.

- Windows:
  `C:\ProgramData\QualiSystems\CloudshellUserSync\Logs\UserSync.log`
- Linux:
  `/opt/CloudshellUserSync/Logs/UserSync.log`

### Dependencies

- `cloudshell-automation-api` to update cloudshell groups
- [LDAP3](https://github.com/cannatag/ldap3) for pulling source LDAP/AD data
- [Schedule](https://github.com/dbader/schedule) as cross-platform cron-like scheduler
- [Keyring](https://github.com/philipn/python-keyring-lib) to store credentials in OS
- [Dacite](https://github.com/konradhalas/dacite) for json to dataclass conversion
- [Pywin32](https://github.com/mhammond/pywin32) - windows service installer util script

### License

Free Software: MIT License