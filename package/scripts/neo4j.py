import os
import base64
from time import sleep
from resource_management import *

class Neo4jMaster(Script):
    
    def install(self, env):
        Execute('cd /tmp && wget http://debian.neo4j.org/neotechnology.gpg.key && rpm --import neotechnology.gpg.key')
        File("/etc/yum.repos.d/neo4j.repo",
             content=Template("neo4j.repo.j2"),
             mode=0o644
             )
        Execute('yum install -y neo4j')             

    def configure(self, env):  
        import params
        env.set_params(params)
        server_cnf_content = InlineTemplate(params.server_cnf_content)   
        File(format("/etc/neo4j/neo4j.conf"), content=server_cnf_content)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('neo4j start', ignore_failures=True)

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute('neo4j stop', ignore_failures=True)


    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/var/run/neo4j/neo4j.pid")


if __name__ == "__main__":
    Neo4jMaster().execute()
