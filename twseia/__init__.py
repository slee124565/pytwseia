"""
import twseia
sa = twseia.SmartApplication('/dev/ttyUSB1')
sa.read_capability()
sa.read
sa.write
"""

from .smart_application import SmartApplication