# Stochastic Character Mapping: An Under-Exploited Approach to the Study of Molecular Evolution

**Simon Laurin-Lemay, Nicolas Rodrigue**

---

## 0. Get Started

```bash
git clone https://github.com/Simonll/Stochastic-character-mapping.git
cd Stochastic-character-mapping
```

---

## 1. Set Up the Conda Environment

```bash
conda env create -f environment.yml
conda activate mappings
```

This includes:

* [bintools](https://github.com/Simonll/bintools.git) — our custom toolkit
* A specific development version of [cogent3](https://github.com/cogent3/cogent3/releases/tag/2024.7.19a7)

---

## 2. Install Docker

Follow the official instructions here:
👉 [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

---

## 3. Build Required Docker Containers

To run the full workflow, build the following Docker containers:

---

### 3.1 Primary Docker Layer

```bash
docker build \
  --build-arg USER_NAME=$(whoami) \
  --build-arg USER_ID=$(id -u ${USER}) \
  --build-arg GROUP_ID=$(id -g ${USER}) \
  -t ubuntu20.04/basic:latest \
  https://github.com/Simonll/docker.git#develop:/dockerfiles/basic --pull
```

---

### 3.2 Phylogenetic Simulator Layer

```bash
docker build \
  --build-arg CACHEBUST=$(date +%s) \
  -t ubuntu20.04/lfp:latest \
  https://github.com/Simonll/docker.git#develop:/dockerfiles/LikelihoodFreePhylogenetics
```

---

### 3.3 PhyloBayes-MPI with Mapping Statistics

```bash
docker build \
  --build-arg CACHEBUST=$(date +%s) \
  -t ubuntu20.04/pbmpi_mapstats:latest \
  https://github.com/Simonll/docker.git#develop:/dockerfiles/phylobayes-mpi/mapstats
```

---

You're now ready to play!
