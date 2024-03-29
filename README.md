🤖 **docker_bridge** 🐳<br>

This is a small program for translating http requests to the docker API.<br>
Its purpose is to protect 🛡 the OS from vertical privilege escalation vulnerabilities.<br>
The program also limits the pool of queries and methods that can be used. Only GET requests are available.<br>

⚠️The program listens to port 10070 after installation.⚠️<br>

Created for use with zabbix http-agent since zabbix-agent2 requires elevated privileges to monitor docker metrics.<br><br>

✅**List of allowed requests**✅<br>

"/docker_containers_all": "containers/json?all=true",<br>
"/docker_containers_not_all": "containers/json?all=false",<br>
"/docker_data_usage":"system/df",<br>
"/docker_images": "images/json",<br>
"/docker_info": "info",<br>
"/docker_ping": "_ping",<br>
"/docker_container_info/{container_id}": "containers/{container_id}/json"<br>
"/docker_container_stats/{container_id}": "/containers/{container_id}/stats?stream=false"<br><br>


🔗**Example of use after installation**🔗<br>
curl http://yours-domain.com:10070/docker_ping<br><br>


⚙️**OS Requirements:**⚙️<br>
1) systemd (if not, the binary file is posted)<br>
2) glibc>=2.17 (ubuntu 13.04, redhat 7)<br><br>
