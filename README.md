# NGS Variant Calling Pipeline

A Python-based Next Generation Sequencing (NGS) pipeline that processes raw FASTQ files and identifies genomic variants by comparing them against a reference genome. The pipeline produces a VCF file containing detected variants.

## Pipeline Overview

The pipeline consists of 9 steps:

0. **Pre-processing** — Automatically detects and decompresses gzipped reference genome files (.gz) to ensure compatibility with downstream tools like bcftools.
1. **Quality Control (FastQC)** — Evaluates the quality of raw FASTQ data, calculates quality scores, and detects adapter sequences.
2. **Adapter Trimming & Filtering (fastp)** — Removes adapter sequences, low-quality bases, and low-quality reads.
3. **Reference Indexing (BWA index)** — Creates an index of the reference FASTA file, similar to a book's index, allowing BWA to quickly locate positions during alignment.
4. **Alignment (BWA mem)** — Aligns the trimmed reads against the reference genome and produces a SAM file.
5. **SAM to BAM Conversion (SAMtools view)** — Converts the SAM file to binary BAM format to reduce file size and enable compatibility with downstream tools.
6. **BAM Sorting (SAMtools sort)** — Sorts the BAM file by chromosomal position.
7. **BAM Indexing (SAMtools index)** — Indexes the sorted BAM file so that tools like bcftools can jump directly to relevant positions without reading the entire file.
8. **Pileup Generation (bcftools mpileup)** — For each position in the genome, calculates how many reads were observed, which bases were seen, and performs statistical variant calculations.
9. **Variant Calling (bcftools call)** — Converts the pileup data into a standard VCF format, reporting variant positions, genotypes, and quality scores.

## Requirements

- Docker

No other dependencies are required. Docker packages all necessary bioinformatics tools (BWA, SAMtools, bcftools, fastp, FastQC) inside the container.

## Usage

### Pull the Docker image

```bash
docker pull ghcr.io/ookaba/ngs-pipeline:latest
```

### Run the pipeline

```bash
docker run --rm \
  -v $(pwd):/data \
  ghcr.io/ookaba/ngs-pipeline:latest run \
  /data/input.fastq \
  /data/ref.fa \
  /data/results
```

Replace `input.fastq` and `ref.fa` with your actual file names.

### Run with AWS CloudWatch logging

```bash
docker run --rm \
  --log-driver=awslogs \
  --log-opt awslogs-region=eu-central-1 \
  --log-opt awslogs-group=ngs-pipeline \
  --log-opt awslogs-create-group=true \
  -v $(pwd):/data \
  ghcr.io/ookaba/ngs-pipeline2:latest run \
  /data/input.fastq \
  /data/ref.fa \
  /data/results
```

## Output

The pipeline produces the following files in the output directory:

- `qc_reports/` — FastQC and fastp quality reports
- `trimmed.fastq` — Adapter-trimmed and quality-filtered reads
- `aligned.sam` — Alignment results in SAM format
- `aligned.bam` — Alignment results in BAM format
- `aligned_sorted.bam` — Sorted BAM file
- `variants.vcf` — Final variant calls in VCF format

## Running Tests

```bash
poetry install
poetry run pytest
```

## CI/CD

This project uses GitHub Actions for continuous integration and delivery:

- **Test job** — On every push, runs pytest to verify code correctness.
- **Docker job** — If tests pass, builds and pushes the Docker image to GitHub Container Registry (`ghcr.io`).

## AWS Deployment

The pipeline was deployed on AWS using the following services:

- **S3** — Storage for input FASTQ/FASTA files and output results.
- **EC2** — Virtual machine for running the Docker container.
- **IAM** — Role-based access control following the least privilege principle. EC2 is granted only S3 read/write permissions.
- **CloudWatch** — Pipeline logs are shipped automatically using Docker's `awslogs` log driver.

## Project Structure

```
ngs-pipeline/
├── src/ngs_pipeline/
│   ├── pipeline.py      # Core pipeline logic
│   └── cli.py           # Command line interface (Click)
├── tests/
│   └── test_pipeline.py # Unit tests
├── Dockerfile
├── pyproject.toml
└── .github/workflows/
    └── ci.yml           # GitHub Actions CI/CD
```
