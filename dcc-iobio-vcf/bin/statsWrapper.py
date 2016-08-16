#!/usr/bin/python
#
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

import sys
import json
import subprocess
import os
import math

arg1 = sys.argv[1]
arg2 = sys.argv[2]
input_json = json.loads(arg1)

precision = 50000
sam_regions = []
previous_region = ''

for region in input_json:
    start_rounded = int(math.floor(region['start']/precision) * precision)
    end_rounded = int(math.ceil(region['end']/precision) * precision)
    
    if end_rounded == start_rounded:
        end_rounded = start_rounded + precision
    
    new_arg = str(region['chr']) + ':' + str(start_rounded) + '-' + str(end_rounded)
    
    # Ensure we are not duplicating rounded regions
    if new_arg != previous_region:
        sam_regions.append(new_arg)
        previous_region = new_arg

path = ""
try: 
    if (os.stat("/home/iobio/iobio/tools/icgc-storage-client/data/collab/" + arg2).st_size != 0):
        path="/home/iobio/iobio/tools/icgc-storage-client/data/collab/" + arg2
    else:
        path="/home/iobio/iobio/tools/icgc-storage-client/data/aws/" + arg2
except OSError:
    path="/home/iobio/iobio/tools/icgc-storage-client/data/aws/" + arg2

bsa_cmd = ["/home/iobio/iobio/bin/vcfstatsalive", "-u", "1000"]
st_cmd = ["/home/iobio/iobio/bin/tabix", "-h", path]
st_cmd.extend(sam_regions)

st = subprocess.Popen(st_cmd, stdout=subprocess.PIPE)
bsa = subprocess.Popen(bsa_cmd, stdin=st.stdout)
bsa.communicate()