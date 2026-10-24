"""Explicit environment selection; default remains the neutral engineering fixture."""
import json
import os
from pathlib import Path
KIND=os.environ.get("EDI_ENGINEERING_WORLD","neutral")
if KIND=="neutral":
    from neutral_world import MISSION, start_world
    PUBLIC_OPERATIONS=None
    def broker_snapshot(out):return json.loads((Path(out)/"world-session.json").read_bytes())
elif KIND=="cedar":
    from meadows_world import MISSION, PUBLIC_OPERATIONS, start_world, broker_snapshot
else:
    raise ValueError("Unsupported explicit engineering world")
