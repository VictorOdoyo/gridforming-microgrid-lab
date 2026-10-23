"""Command-line entry point for reproducible engineering experiments."""
import argparse
from dataclasses import replace
import json
from .cases import CASES
from .config_io import load_case
from .events import run_events

def parser():
    p = argparse.ArgumentParser(prog="gridlab", description="Grid-forming microgrid simulation laboratory")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list built-in experiments")
    run = sub.add_parser("run", help="simulate a case and write a report directory")
    source = run.add_mutually_exclusive_group()
    source.add_argument("--case", choices=sorted(CASES), default=None)
    source.add_argument("--config", help="JSON or TOML case")
    run.add_argument("--mode", choices=("droop", "vsm"), default=None)
    run.add_argument("--duration", type=float)
    run.add_argument("--sample", type=float, default=.02, help="output sampling interval in seconds")
    run.add_argument("--max-step", type=float, default=.02, help="maximum integrator step in seconds")
    run.add_argument("--output", default="outputs/run")
    stability = sub.add_parser("stability", help="linearize a built-in case at synchronous equilibrium")
    stability.add_argument("--case", choices=sorted(CASES), default="load-step")
    stability.add_argument("--mode", choices=("droop", "vsm"), default="droop")
    return p

def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    try:
        if args.command == "list":
            for name, factory in sorted(CASES.items()):
                print(f"{name}: {factory().description}")
            return 0
        if args.command == "stability":
            from .stability import stability_report
            case = CASES[args.case](args.mode)
            print(json.dumps(stability_report(case.config), indent=2))
            return 0
        if args.command == "run":
            case = load_case(args.config) if args.config else CASES[args.case or "load-step"](args.mode or "droop")
            if args.mode and args.config:
                case = replace(case, config=replace(case.config,
                               inverters=tuple(replace(i, mode=args.mode) for i in case.config.inverters)))
            if args.duration is not None:
                case = replace(case, duration=args.duration,
                               events=tuple(e for e in case.events if e.time <= args.duration))
            trace = run_events(case.config, case.events, case.duration, args.sample, max_step=args.max_step)
            from .report import write_report
            metrics = write_report(case, trace, args.output)
            print(json.dumps({"case": case.name, "output": args.output, "metrics": metrics}, indent=2))
            return 0
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as exc:
        p.error(str(exc))
    return 0
