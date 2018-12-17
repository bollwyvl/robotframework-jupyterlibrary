import subprocess
import sys
from os.path import join

# import for PATH side-effect. yuck.
import chromedriver_binary  # noqa

from . import BROWSER, HERE, PLATFORM, TEST_OUT, TESTS


def run_tests(robot_args):
    args = (
        [
            "python",
            "-m",
            "robot",
            "-d",
            TEST_OUT,
            "--log",
            join(TEST_OUT, join(".".join([PLATFORM, BROWSER, "log", "html"]))),
            "--name",
            "{} on {}".format(BROWSER, PLATFORM),
            "--output",
            join(TEST_OUT, join(".".join([PLATFORM, BROWSER, "robot", "xml"]))),
            "--report",
            join(TEST_OUT, join(".".join([PLATFORM, BROWSER, "report", "html"]))),
            "--variable",
            "BROWSER:" + BROWSER,
            "--variable",
            "OS:" + PLATFORM,
            "--xunit",
            ".".join([PLATFORM, BROWSER, "robot", "xunit", "xml"]),
        ]
        + robot_args
        + [TESTS]
    )

    print(" ".join(args))
    proc = subprocess.Popen(args, cwd=HERE)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        proc.kill()
        return proc.wait()


if __name__ == "__main__":
    sys.exit(run_tests(sys.argv[1:]))