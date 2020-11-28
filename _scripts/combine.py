import sys
import subprocess

from . import project as P


def combine():
    final = P.ATEST_OUT / P.ATEST_OUT_XML

    all_files = sorted(P.ATEST_OUT.rglob(P.ATEST_OUT_XML))
    all_output_dirs = sorted({p.parent for p in all_files})
    [print(f"- {p.relative_to(P.ATEST_OUT)}") for p in all_output_dirs]

    all_robot = [
        p
        for p in P.ATEST_OUT.rglob(P.ATEST_OUT_XML)
        if p != final and "pabot_results" not in str(p)
    ]
    args = [
        "python",
        "-m",
        "robot.rebot",
        "--name",
        P.SETUP["metadata"]["name"],
        "--metadata",
        f"""version:{P.VERSION}""",
        "--outputdir",
        P.ATEST_OUT,
        "--output",
        P.ATEST_OUT_XML,
    ] + all_robot

    str_args = [*map(str, args)]

    print(">>> rebot args: ", " ".join(str_args), flush=True)

    proc = subprocess.Popen(str_args)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


if __name__ == "__main__":
    sys.exit(combine())
