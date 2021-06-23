# This is a short example of how to setup this server
# Note: this server must be ran on an Ansible node and provision another machine
Relevant Link:
[ansible-runner](https://ansible-runner.readthedocs.io/en/latest/index.html)
__Document Structure__
.
├── env
│&nbsp;&nbsp; ├── envvars
│&nbsp;&nbsp; ├── extravars
│&nbsp;&nbsp; ├── passwords
│&nbsp;&nbsp; ├── cmdline
│&nbsp;&nbsp; ├── settings
│&nbsp;&nbsp; └── ssh_key
├── inventory
│&nbsp;&nbsp; └── hosts
└── project
 &nbsp;&nbsp; ├── test.yml
    └── roles
        └── testrole
            ├── defaults
            ├── handlers
            ├── meta
            ├── README.md
            ├── tasks
            ├── tests
            └── vars

