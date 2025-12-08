import gc
import time
from dataclasses import dataclass

gc.set_debug(gc.DEBUG_STATS)


@dataclass(slots=True)
class RunState:
    current_mode: str = "init"


def init_state():
    return RunState()


def gc_logger(phase, info):
    if phase == "start":
        gen = info["generation"]
        if hasattr(gc_logger, "state") and gc_logger.state is not None:
            print(
                f"GC collecting Gen{gen} (triggered during {gc_logger.state.current_mode})"
            )
        else:
            print(f"GC collecting Gen{gen} (no state attached)")


gc.callbacks.append(gc_logger)


def gc_demo(iterations=1025, state=None):
    if state is None:
        state = init_state()

    gc_logger.state = state
    for i in range(iterations):
        outer_list = [list(range(5)) for _ in range(5)]
        nested = [outer_list, outer_list[::-1]]

        mode = i % 4
        if mode == 0:
            state.current_mode = "Mode 0: slice both"
            outer_list[:] = []
            nested[:] = []
        elif mode == 1:
            state.current_mode = "Mode 1: slice outer, redeclare nested"
            outer_list[:] = []
            nested = []
        elif mode == 2:
            state.current_mode = "Mode 2: redeclare outer, slice nested"
            outer_list = []
            nested[:] = []
        else:
            state.current_mode = "Mode 3: redeclare both"
            outer_list = []
            nested = []

        if i % 200 == 0:
            g0, g1, g2 = gc.get_count()
            print(
                f"[{i}] {state.current_mode} | Counters Gen0={g0}, Gen1={g1}, Gen2={g2}"
            )
            time.sleep(0.01)


gc_demo()
