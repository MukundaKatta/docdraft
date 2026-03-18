"""Tests for Docdraft."""
from src.core import Docdraft
def test_init(): assert Docdraft().get_stats()["ops"] == 0
def test_op(): c = Docdraft(); c.generate(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Docdraft(); [c.generate() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Docdraft(); c.generate(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Docdraft(); r = c.generate(); assert r["service"] == "docdraft"
