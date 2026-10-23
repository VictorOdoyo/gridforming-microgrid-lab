"""CLI for coupled physical laboratory experiments."""

import json
from pathlib import Path

from .case import run_case
from .cases import CASES
from .config_io import load_case, parse_case, save_case
from .timing import retime


def add_parser(sub):
    lab = sub.add_parser("lab", help="run SI battery/converter/hybrid experiments")
    commands = lab.add_subparsers(dest="lab_command", required=True)
    commands.add_parser("list", help="list physical experiments")
    run = commands.add_parser("run", help="simulate and save a complete physical report")
    source = run.add_mutually_exclusive_group()
    source.add_argument("--case", choices=sorted(CASES), default=None)
    source.add_argument("--config")
    run.add_argument("--duration", type=float)
    run.add_argument("--period", type=float)
    run.add_argument("--output", default="outputs/lab")
    export = commands.add_parser("export-case", help="save an editable physical case")
    export.add_argument("--case", choices=sorted(CASES), default="hybrid-step")
    export.add_argument("--output", required=True)
    inspect = commands.add_parser("inspect", help="summarize a physical trace archive")
    inspect.add_argument("input")
    study = commands.add_parser("study", help="run sampled-control and physical-model studies")
    study.add_argument("kind", choices=("sample-delay", "dc-convergence", "observer", "active-damping"))
    study.add_argument("--output", default="outputs/physical-study.json")


def execute(args):
    if args.lab_command == "list":
        for name, factory in sorted(CASES.items()):
            case = factory()
            print(f"{name} [{case.kind}]: {case.description}")
        return 0
    if args.lab_command == "study":
        from gridlab.converter.delay_study import delay_study
        from gridlab.provenance import provenance

        from .damping_study import damping_study
        from .dc_convergence import dc_convergence
        from .observer_study import observer_study

        functions = {
            "sample-delay": delay_study,
            "dc-convergence": dc_convergence,
            "observer": observer_study,
            "active-damping": damping_study,
        }
        record = {
            "study": args.kind,
            "results": functions[args.kind](),
            "provenance": provenance(CASES["hybrid-step"]()),
        }
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(record, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        print(json.dumps({"study": args.kind, "output": str(target)}))
        return 0
    if args.lab_command == "export-case":
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        save_case(CASES[args.case](), path)
        print(path)
        return 0
    if args.lab_command == "inspect":
        from .metrics import summarize
        from .storage import load_trace

        _, trace, metadata = load_trace(args.input)
        case = parse_case(metadata["case"])
        print(json.dumps(summarize(case, trace), indent=2, allow_nan=False))
        return 0
    case = load_case(args.config) if args.config else CASES[args.case or "hybrid-step"]()
    case = retime(case, args.duration, args.period)
    trace = run_case(case)
    from .report import write_report

    metrics = write_report(case, trace, args.output)
    print(
        json.dumps({"case": case.name, "output": args.output, "metrics": metrics}, indent=2, allow_nan=False)
    )
    return 0
