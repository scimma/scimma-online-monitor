###
### Author: ree55@psu.edu
### Date:   Oct 8, 2023
### Desc:   Build a container that stores scimma usage metrics to Influx
###
FROM scimma/client:0.7.1
RUN  mkdir -p /usr/local/src
RUN yum -y install git unzip python3-pytz.noarch python38-pytz.noarch
RUN cd /usr/local/src && \
    curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws

# install ligo-scald
RUN cd /usr/local/src && \
    git clone https://$gitlab_name:$gitlab_token@git.ligo.org/gstlal-visualisation/ligo-scald.git && \
    cd ligo-scald && \
    python3 setup.py install --prefix /usr --root / --single-version-externally-managed

# ADD scald configiguration file
ADD config/scald.yml config/scald.yml

# ADD script
ADD scripts/helloworld.py /root/helloworld.py
RUN chmod ugo+rx /root/helloworld.py

WORKDIR /tmp
ENTRYPOINT ["/root/helloworld.py"]
