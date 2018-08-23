# Copyright 2018 China UnionPay.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from zun.common import context
from zun import objects
from zun.scheduler.filters import cup_cpuset_filter
from zun.tests import base
from zun.tests.unit.scheduler import fakes


class TestCUP_CPUSETFilter(base.TestCase):
    def setUp(self):
        super(TestCUP_CPUSETFilter, self).setUp()
        self.context = context.RequestContext('fake_user', 'fake_project')

    def testcup_cpuset_filter_pass(self):
        self.filt_cls = cup_cpuset_filter.CUP_CPUSETFilter(self.context)
        container = objects.Container(self.context)
        container.cpu_policy = 'dedicated'
        container.cpu = 2.0
        container.memory = '1024M'
        host = fakes.FakeHostState('testhost')
        host.cpus = 6
        host.cpu_used = 0.0
        host.numa_topology = objects.NUMATopology(cells=[
            objects.NUMANode(id=0, cpuset=set([1, 2, 3]), pinned_cpus=set([]), mem_total=32739, mem_available=32739),
            objects.NUMANode(id=1, cpuset=set([4, 5, 6]), pinned_cpus=set([]), mem_total=32739, mem_available=32739)]
        )
        extra_spec = {}
        self.assertTrue(self.filt_cls.host_passes(host, container, extra_spec))

    def testcup_cpuset_filter_fail(self):
        self.filt_cls = cup_cpuset_filter.CUP_CPUSETFilter(self.context)
        container = objects.Container(self.context)
        container.cpu_policy = 'dedicated'
        container.cpu = 4.0
        container.memory = '1024M'
        host = fakes.FakeHostState('testhost')
        host.cpus = 6
        host.cpu_used = 0.0
        host.numa_topology = objects.NUMATopology(cells=[
            objects.NUMANode(id=0, cpuset=set([1, 2, 3]), pinned_cpus=set([]), mem_total=32739, mem_available=32739),
            objects.NUMANode(id=1, cpuset=set([4, 5, 6]), pinned_cpus=set([]), mem_total=32739, mem_available=32739)]
        )
        extra_spec = {}
        self.assertTrue(self.filt_cls.host_passes(host, container, extra_spec))
