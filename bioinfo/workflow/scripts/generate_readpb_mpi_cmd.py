import argparse
import os
import re
from typing import Dict

from bintools.run.run import generate_pb_mpi_cmd


def generate_mapping(dir_a: str, dir_b: str, input: str) -> str:
    s: str = dir_b + re.sub(dir_a, "", input)
    return s


def wrapper(
    input: str,
    model: str,
    np: str,
    image: str,
    sampling: str,
    local_root: str,
    docker_root: str,
    cluster_root: str,
    work_dir: str,
    sh_docker: str,
    sh_cluster: str,
) -> str:

    os.makedirs(
        os.path.dirname(local_root + work_dir) + "/",
        exist_ok=True,
    )

    logger_local: str = " ".join(
        [
            "2>",
            local_root + work_dir + sh_docker[:-3] + ".log",
        ]
    )
    cmd: str = ""
    kwargs: Dict[str, str] = {}
    # if not model.startswith("F81"):
    kwargs = {
        "-np": str(2),
        "-x": sampling,
        model: "",
        "-chainname": generate_mapping(
            dir_a=local_root, dir_b=docker_root, input=input[:-6]
        ),
    }
    cmd = generate_pb_mpi_cmd(
        method="readpb_mpi",
        mapping=local_root + ":" + docker_root,
        logger=logger_local,
        image=image,
        **kwargs
    )

    with open(local_root + work_dir + sh_docker, "w") as fh:
        fh.write(cmd)

    with open(local_root + work_dir + sh_cluster, "w") as fh:
        fh.write(
            "#qsub -cwd -pe mpi %s %s"
            % (np, cluster_root + work_dir + sh_cluster + "\n")
        )
        fh.write("LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:$LD_LIBRARY_PATH\n")
        fh.write("CXX=`which g++`\n")
        fh.write("CC=`which gcc`\n")
        fh.write("export LD_LIBRARY_PATH\n")
        fh.write("export CC\n")
        fh.write("export CXX\n")
        fh.write(
            "mpirun -np %s /home/sll/pbmpi-versions/submap/pbmpi/data/readpb_mpi %s -x %s %s"
            % (
                np,
                model,
                sampling,
                generate_mapping(dir_a=local_root, dir_b=cluster_root, input=input[:-6]),
            )
        )

    return cmd


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="argument", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--image",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--sampling",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--np",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--local_root",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--docker_root",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--cluster_root",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--work_dir",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--sh_docker",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--sh_cluster",
        type=str,
        required=True,
    )

    args = parser.parse_args()
    wrapper(
        input=args.input,
        model=args.model,
        image=args.image,
        sampling=args.sampling,
        np=args.np,
        local_root=args.local_root,
        docker_root=args.docker_root,
        cluster_root=args.cluster_root,
        work_dir=args.work_dir,
        sh_cluster=args.sh_cluster,
        sh_docker=args.sh_docker,
    )
