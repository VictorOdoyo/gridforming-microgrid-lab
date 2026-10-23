"""Command-line entry point for reproducible engineering experiments."""

import argparse
import json
from dataclasses import replace

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
    run.add_argument("--sample", type=float, default=0.02, help="output sampling interval in seconds")
    run.add_argument("--max-step", type=float, default=0.02, help="maximum integrator step in seconds")
    run.add_argument("--output", default="outputs/run")
    stability = sub.add_parser("stability", help="linearize a built-in case at synchronous equilibrium")
    stability.add_argument("--case", choices=sorted(CASES), default="load-step")
    stability.add_argument("--mode", choices=("droop", "vsm"), default="droop")
    compare = sub.add_parser("compare", help="compare droop and VSM under the same load step")
    compare.add_argument("--duration", type=float, default=8)
    compare.add_argument("--output", default="outputs/comparison")
    study = sub.add_parser("study", help="run an engineering parameter or energy study")
    study.add_argument(
        "kind", choices=("weak-grid", "stability-map", "daily-energy", "convergence", "robustness")
    )
    study.add_argument("--output", default="outputs/study.json")
    study.add_argument("--count", type=int, default=12, help="uncertainty trial count")
    study.add_argument("--seed", type=int, default=42)
    export = sub.add_parser("export-case", help="export a built-in case for editing")
    export.add_argument("--case", choices=sorted(CASES), default="load-step")
    export.add_argument("--mode", choices=("droop", "vsm"), default="droop")
    export.add_argument("--output", required=True)
    inspect = sub.add_parser("inspect", help="summarize a saved NumPy trace")
    inspect.add_argument("input")
    return p


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    try:
        if args.command == "list":
            for name, factory in sorted(CASES.items()):
                print(f"{name}: {factory().description}")
            return 0
        if args.command == "export-case":
            from pathlib import Path

            from .config_io import save_case

            path = Path(args.output)
            path.parent.mkdir(parents=True, exist_ok=True)
            save_case(CASES[args.case](args.mode), path)
            print(str(path))
            return 0
        if args.command == "inspect":
            from .storage import load_result
            from .summary import summarize

            print(json.dumps(summarize(load_result(args.input)), indent=2, allow_nan=False))
            return 0
        if args.command == "study":
            from dataclasses import asdict, is_dataclass
            from pathlib import Path

            from .daily_energy import daily_energy
            from .integration_study import integration_study
            from .robustness import robustness_study
            from .stability_sweep import stability_sweep
            from .weak_grid import weak_grid_study

            functions = {
                "weak-grid": weak_grid_study,
                "stability-map": stability_sweep,
                "daily-energy": daily_energy,
                "convergence": integration_study,
                "robustness": lambda: robustness_study(args.count, args.seed),
            }
            value = functions[args.kind]()

            def serialize(obj):
                if is_dataclass(obj):
                    return asdict(obj)
                raise TypeError(f"unsupported study value: {type(obj).__name__}")

            content = json.dumps(value, indent=2, default=serialize, allow_nan=False)
            path = Path(args.output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content + "\n", encoding="utf-8")
            print(json.dumps({"study": args.kind, "output": str(path)}))
            return 0
        if args.command == "compare":
            from pathlib import Path

            from .cases import load_step
            from .comparison import compare_controls
            from .report import write_report

            results = compare_controls(args.duration)
            summaries = {}
            for mode, value in results.items():
                base = load_step(mode)
                case = replace(
                    base,
                    duration=args.duration,
                    events=tuple(e for e in base.events if e.time <= args.duration),
                )
                summaries[mode] = write_report(case, value["trace"], Path(args.output) / mode)
            print(json.dumps(summaries, indent=2))
            return 0
        if args.command == "stability":
            from .stability import stability_report

            case = CASES[args.case](args.mode)
            print(json.dumps(stability_report(case.config), indent=2))
            return 0
        if args.command == "run":
            case = (
                load_case(args.config)
                if args.config
                else CASES[args.case or "load-step"](args.mode or "droop")
            )
            if args.mode and args.config:
                case = replace(
                    case,
                    config=replace(
                        case.config,
                        inverters=tuple(replace(i, mode=args.mode) for i in case.config.inverters),
                    ),
                )
            if args.duration is not None:
                case = replace(
                    case,
                    duration=args.duration,
                    events=tuple(e for e in case.events if e.time <= args.duration),
                )
            trace = run_events(case.config, case.events, case.duration, args.sample, max_step=args.max_step)
            from .report import write_report

            metrics = write_report(case, trace, args.output)
            print(json.dumps({"case": case.name, "output": args.output, "metrics": metrics}, indent=2))
            return 0
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as exc:
        p.error(str(exc))
    return 0
