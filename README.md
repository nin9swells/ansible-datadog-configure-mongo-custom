aansible-datadog-configure-custom-mongo-checks

Ansible Role to configure Datadog Agent Custom MongoDB Checks

It will collect these metrics:
- custom.mongodb.curr_op_5s: the count of running operations that have been run for >= 5 seconds (with tags "ismaster" and "replset_name" (for replica set))
- custom.mongodb.curr_op_15s the count of running operations that have been run for >= 15 seconds (with tags "ismaster" and "replset_name" (for replica set))
- custom.mongodb.curr_op_30s the count of running operations that have been run for >= 30 seconds (with tags "ismaster" and "replset_name" (for replica set))

It's related to this doc: https://docs.datadoghq.com/guides/agent_checks/
This role contains two parts:
- Adding custom MongoDB checks
- Removing custom MongoDB checks

Installing / Uninstalling Datadog Custom MongoDB Checks

For installation, it will add file custom-mongo.yaml and custom-mongo.py.
For uninstallation, it will remove file custom-mongo.yaml and custom-mongo.py.

Required Variables

None

Additional Variables
- custom_check_state
  desc: present, absent
  default: present

- check_config:
  desc: The value for custom-mongo.yaml, you don't need this if "custom_check_state" is "absent". If you set this, there are 2 attributes that you can specify:
  - "init_config"
    you can set attribute "min_collection_interval" (optional), there is a brief explanation at https://docs.datadoghq.com/guides/agent_checks/#configuration
  - "instances"
    you can set attribute:
    - "server" (mandatory), this is the MongoDB URL to connect to

Testing

There are 2 options of testing:
- Installation (test_present.yml)
- Uninstallation (test_absent.yml)

To testing using vagrant for those options, use:

TASK='task_name' vagrant up

task_name value : test_present.yml, test_absent.yml
