# compose-pydantic

Parse `Compose Specification` YAML using `Pydantic` and `PyYAML`.

## Description

This library works as a thin layer on top of `pydantic`. It's purpose is to convert YAML to Python objects.
The python model is generated using `datamodel-codegen` and the `Compose Specification` JSON schema URI.
```bash
datamodel-codegen \
    --input-file-type jsonschema \
    --url https://raw.githubusercontent.com/compose-spec/compose-spec/master/schema/compose-spec.json \
    --output compose_pydantic/models.py
```

## Getting Started

### Dependencies

* pydantic==1.9.0
* PyYAML>=6.0
* mergedeep>=1.3.4

### Installation

```bash
pip install compose-pydantic
```

### Usage

Read multiple compose files
```python
from compose_pydantic import ComposeSpecificationFactory

csf = ComposeSpecificationFactory()
compose = csf(source='tests/compose/docker-compose.yml', overrides=['tests/compose/docker-compose.override.yml'])

print(compose.__dict__)
```

Result:
```python
{'version': '3.9', 'name': None, 'services': {'db': Service(deploy=None, build=None, blkio_config=None, cap_add=None, cap_drop=None, cgroup_parent=None, command=None, configs=None, container_name=None, cpu_count=None, cpu_percent=None, cpu_shares=None, cpu_quota=None, cpu_period=None, cpu_rt_period=None, cpu_rt_runtime=None, cpus=None, cpuset=None, credential_spec=None, depends_on=None, device_cgroup_rules=None, devices=None, dns=None, dns_opt=None, dns_search=None, domainname=None, entrypoint=None, env_file=None, environment=ListOrDict(__root__=['POSTGRES_NAME=devpostgres', 'POSTGRES_USER=devpostgres', 'POSTGRES_PASSWORD=devpostgres']), expose=None, extends=None, external_links=None, extra_hosts=None, group_add=None, healthcheck=None, hostname=None, image='postgres', init=None, ipc=None, isolation=None, labels=None, links=None, logging=None, mac_address=None, mem_limit=None, mem_reservation=None, mem_swappiness=None, memswap_limit=None, network_mode=None, networks=None, oom_kill_disable=None, oom_score_adj=None, pid=None, pids_limit=None, platform=None, ports=None, privileged=None, profiles=None, pull_policy=None, read_only=None, restart=None, runtime=None, scale=None, security_opt=None, shm_size=None, secrets=None, sysctls=None, stdin_open=None, stop_grace_period=None, stop_signal=None, storage_opt=None, tmpfs=None, tty=None, ulimits=None, user=None, userns_mode=None, volumes=['./data/db:/var/lib/postgresql/data'], volumes_from=None, working_dir=None), 'web': Service(deploy=None, build='.', blkio_config=None, cap_add=None, cap_drop=None, cgroup_parent=None, command='python manage.py runserver 0.0.0.0:8000', configs=None, container_name=None, cpu_count=None, cpu_percent=None, cpu_shares=None, cpu_quota=None, cpu_period=None, cpu_rt_period=None, cpu_rt_runtime=None, cpus=None, cpuset=None, credential_spec=None, depends_on=ListOfStrings(__root__=['db']), device_cgroup_rules=None, devices=None, dns=None, dns_opt=None, dns_search=None, domainname=None, entrypoint=None, env_file=None, environment=ListOrDict(__root__=['POSTGRES_NAME=devpostgres', 'POSTGRES_USER=devpostgres', 'POSTGRES_PASSWORD=devpostgres']), expose=None, extends=None, external_links=None, extra_hosts=None, group_add=None, healthcheck=None, hostname=None, image=None, init=None, ipc=None, isolation=None, labels=None, links=None, logging=None, mac_address=None, mem_limit=None, mem_reservation=None, mem_swappiness=None, memswap_limit=None, network_mode=None, networks=None, oom_kill_disable=None, oom_score_adj=None, pid=None, pids_limit=None, platform=None, ports=['8000:8000'], privileged=None, profiles=None, pull_policy=None, read_only=None, restart=None, runtime=None, scale=None, security_opt=None, shm_size=None, secrets=None, sysctls=None, stdin_open=None, stop_grace_period=None, stop_signal=None, storage_opt=None, tmpfs=None, tty=None, ulimits=None, user=None, userns_mode=None, volumes=['.:/code'], volumes_from=None, working_dir=None)}, 'networks': None, 'volumes': None, 'secrets': None, 'configs': None}
```

## Tests

If you're working with a clone of this repository, you can run tests like this:

```bash
$ make init test
```

See also `tests/test_lib.py` for the different ways you may use the factory class to access compose spec data.

## Authors

Alexandros Monastiriotis alexmondev@gmail.com

## Version History

* 0.2.0
    * Change API
* 0.1.1
    * Add missing dependency
* 0.1.0
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

Inspiration, libraries, etc.
* [pydantic](https://github.com/samuelcolvin/pydantic/)
* [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/)
* [Compose Specification](https://github.com/compose-spec/compose-spec)
* [PyYAML](https://github.com/yaml/pyyaml)
* [mergedeep](https://github.com/clarketm/mergedeep)
* [Understanding multiple Compose files](https://docs.docker.com/compose/extends/#multiple-compose-files)
