#     ______________________   ____      __    _          _    ______________
#    /  _/ ____/ ____/ ____/  /  _/___  / /_  (_)___     | |  / / ____/ ____/
#    / // /   / / __/ /       / // __ \/ __ \/ / __ \    | | / / /   / /_    
#  _/ // /___/ /_/ / /___   _/ // /_/ / /_/ / / /_/ /    | |/ / /___/ __/    
# /___/\____/\____/\____/  /___/\____/_.___/_/\____/     |___/\____/_/       
#
# Banner @ http://goo.gl/Uc4YXy

# Copyright (c) 2016 The Ontario Institute for Cancer Research. All rights reserved.                            
#
# This program and the accompanying materials are made available under the terms of the GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along with                                 
# this program. If not, see <http://www.gnu.org/licenses/>.                                                    
#                                                                                                              
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY                          
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES                         
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT                          
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,                               
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED                         
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;                              
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER                             
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN                        
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#                                                                            
# Extend new iobio image
#

FROM qiaoy/iobio-bundle.vcf-iobio:dev

#
# Install java 8
# Based on:
# https://hub.docker.com/r/frolvlad/alpine-glibc/~/dockerfile/
# https://hub.docker.com/r/frolvlad/alpine-oraclejdk8/~/dockerfile/
#

RUN apk add --update wget ca-certificates && \
    export ALPINE_GLIBC_BASE_URL="https://circle-artifacts.com/gh/andyshinn/alpine-pkg-glibc/6/artifacts/0/home/ubuntu/alpine-pkg-glibc/packages/x86_64" && \
    export ALPINE_GLIBC_PACKAGE="glibc-2.21-r2.apk" && \
    export ALPINE_GLIBC_BIN_PACKAGE="glibc-bin-2.21-r2.apk" && \
    wget "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE" "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_BIN_PACKAGE" && \
    apk add --allow-untrusted "$ALPINE_GLIBC_PACKAGE" "$ALPINE_GLIBC_BIN_PACKAGE" && \
    /usr/glibc/usr/bin/ldconfig "/lib" "/usr/glibc/usr/lib" && \
    echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf && \
    apk del wget ca-certificates && \
    rm "$ALPINE_GLIBC_PACKAGE" "$ALPINE_GLIBC_BIN_PACKAGE" /var/cache/apk/*

ENV JAVA_VERSION=8 \
    JAVA_UPDATE=66 \
    JAVA_BUILD=17 \
    JAVA_HOME=/usr/lib/jvm/default-jvm

RUN apk add --update wget ca-certificates && \
    cd /tmp && \
    wget --header "Cookie: oraclelicense=accept-securebackup-cookie;" \
        "http://download.oracle.com/otn-pub/java/jdk/${JAVA_VERSION}u${JAVA_UPDATE}-b${JAVA_BUILD}/jdk-${JAVA_VERSION}u${JAVA_UPDATE}-linux-x64.tar.gz" && \
    tar xzf "jdk-${JAVA_VERSION}u${JAVA_UPDATE}-linux-x64.tar.gz" && \
    mkdir -p "/usr/lib/jvm" && \
    mv "/tmp/jdk1.${JAVA_VERSION}.0_${JAVA_UPDATE}" "/usr/lib/jvm/java-${JAVA_VERSION}-oracle" && \
    ln -s "java-${JAVA_VERSION}-oracle" "$JAVA_HOME" && \
    ln -s "$JAVA_HOME/bin/"* "/usr/bin/" && \
    rm -rf "$JAVA_HOME/"*src.zip && \
    apk del wget ca-certificates && \
    rm -rf /tmp/* /var/cache/apk/*
 
#
# Install lib
#

RUN apk update
RUN apk add fuse fuse-dev

#
# Installing latest dcc-storage-client
#

RUN mkdir -p /home/iobio/iobio/tools/icgc-storage-client && \
    cd /home/iobio/iobio/tools/icgc-storage-client && \
    wget -qO- https://seqwaremaven.oicr.on.ca/artifactory/dcc-release/org/icgc/dcc/icgc-storage-client/[RELEASE]/icgc-storage-client-[RELEASE]-dist.tar.gz | \
    tar xvz

#
# Copies icgc-storage-client folders out one directive
# Alternative for lack of tar strip-components
#

RUN cp -r /home/iobio/iobio/tools/icgc-storage-client/*/* /home/iobio/iobio/tools/icgc-storage-client/

#
# Makes a directory for icgc-storage-client collab and aws to mount
#

RUN mkdir /home/iobio/iobio/tools/icgc-storage-client/data
RUN mkdir /home/iobio/iobio/tools/icgc-storage-client/data/aws
RUN mkdir /home/iobio/iobio/tools/icgc-storage-client/data/collab

#
# Adds necessary files in order to run
#

RUN npm install --prefix /home/iobio/iobio ps-tree
ADD conf/nginx.conf /etc/nginx/nginx.conf
ADD app.conf /etc/supervisor.d/

#
# Use our wrappers
#
ADD bin/vcfReadDeptherHelper.sh /home/iobio/iobio/bin/vcfReadDeptherHelper.sh
ADD bin/vcfstatsAliveWrapper.sh /home/iobio/iobio/bin/vcfstatsAliveWrapper.sh
ADD bin/statsWrapper.py /home/iobio/iobio/bin/statsWrapper.py
RUN chmod +x /home/iobio/iobio/bin/vcfReadDeptherHelper.sh
RUN chmod +x /home/iobio/iobio/bin/vcfstatsAliveWrapper.sh
RUN chmod +x /home/iobio/iobio/bin/statsWrapper.py

ADD services/vcfstatsalive.js /home/iobio/iobio/services/vcfstatsalive.js

#
# Our version of the tabix binary to support idx files
#
RUN rm -rf /home/iobio/iobio/bin/tabix
ADD bin/tabix /home/iobio/iobio/bin/tabix
RUN chmod +x /home/iobio/iobio/bin/tabix

#
# Our version of the vcfstatsalive binary to enfore minimum required variants
#
RUN rm -rf /home/iobio/iobio/bin/vcfstatsalive
ADD bin/vcfstatsalive /home/iobio/iobio/bin/vcfstatsalive
RUN chmod +x /home/iobio/iobio/bin/vcfstatsalive

#
# Modify their backend code
#

ADD lib/cmd.js /home/iobio/iobio/lib/cmd.js
ADD lib/server.js /home/iobio/iobio/lib/server.js

#
# Cleanup some of the executables and services we don't want
#
RUN rm -rf /home/iobio/iobio/bin/bamBinnerHelper.sh
RUN rm -rf /home/iobio/iobio/bin/bamReadDeptherHelper.sh
RUN rm -rf /home/iobio/iobio/bin/bamHelper.sh
RUN rm -rf /home/iobio/iobio/services/bamstatsAliveServer.js
RUN rm -rf /home/iobio/iobio/services/bamReadDepther.js
RUN rm -rf /home/iobio/iobio/services/samtoolsServer.js
RUN rm -rf /home/iobio/iobio/services/tabixServer.js
RUN rm -rf /home/iobio/iobio/services/emailServer.js
RUN rm -rf /home/iobio/iobio/services/bamBinnerServer.js
RUN rm -rf /home/iobio/iobio/services/bamMergerServer.js
RUN rm -rf /home/iobio/iobio/services/bamtoolsServer.js

#
# Add landing page for the server
#
ADD www/index.html /var/www/html/index.html
ADD www/favicon.ico /var/www/html/favicon.ico

#
# Add cleanup script
#
ADD bin/cleaner.sh /home/iobio/iobio/bin/cleaner.sh
RUN chmod +x /home/iobio/iobio/bin/cleaner.sh