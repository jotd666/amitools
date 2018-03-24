from __future__ import print_function
import logging
import pytest

from amitools.vamos.libcore import LibStubGen, LibCtx
from amitools.vamos.lib.VamosTestLibrary import VamosTestLibrary
from amitools.vamos.machine import MockCPU, MockMemory
from amitools.vamos.libcore import LibProfile
from amitools.fd import read_lib_fd


def _create_ctx():
  cpu = MockCPU()
  mem = MockMemory()
  return LibCtx(cpu, mem)


def _create_stub(do_profile=False, do_log=False):
  name = 'vamostest.library'
  impl = VamosTestLibrary()
  fd = read_lib_fd(name)
  ctx = _create_ctx()
  if do_profile:
    profile = LibProfile(name, fd)
  else:
    profile = None
  if do_log:
    log_missing = logging.getLogger('missing')
    log_valid = logging.getLogger('valid')
  else:
    log_missing = None
    log_valid = None
  # create stub
  gen = LibStubGen(log_missing=log_missing, log_valid=log_valid)
  stub = gen.gen_stub(name, impl, fd, ctx, profile)
  return stub


def libcore_stub_base_benchmark(benchmark):
  stub = _create_stub()
  benchmark(stub.PrintHello)


def libcore_stub_profile_benchmark(benchmark):
  stub = _create_stub(do_profile=True)
  benchmark(stub.PrintHello)


def libcore_stub_log_benchmark(benchmark):
  stub = _create_stub(do_log=True)
  benchmark(stub.PrintHello)


def libcore_stub_log_profile_benchmark(benchmark):
  stub = _create_stub(do_profile=True, do_log=True)
  benchmark(stub.PrintHello)
