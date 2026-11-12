"""Run: python skills/skills-doctor/test_doctor.py  (stdlib only)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doctor import strict_yaml_problem

assert strict_yaml_problem("---\nname: x\ndescription: Portable: works anywhere\n---\n")
assert strict_yaml_problem("---\nname: x\ndescription: see notes #2 here\n---\n")
assert strict_yaml_problem("---\nname: x\ndescription: 'Portable: works anywhere'\n---\n") is None
assert strict_yaml_problem("---\nname: x\ndescription: \"a: b\"\n---\n") is None
assert strict_yaml_problem("---\nname: x\ndescription: plain words, no trap\n---\n") is None
assert strict_yaml_problem("---\nname: x\ndescription: url https://a.b/c is fine\n---\n") is None
print("ok")
