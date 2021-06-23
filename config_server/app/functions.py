import ansible_runner
import os

def restart():
    print(os.getcwd())
    r = ansible_runner.run(private_data_dir=os.getenv('PROJ_DIR'), playbook='restart.yaml')
    print("{}: {}".format(r.status, r.rc))

    for event in r.events:
        print(event['event'])
    print("Final status:")
    print(r.stats)
