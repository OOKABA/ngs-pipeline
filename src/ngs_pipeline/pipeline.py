import subprocess
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_command(cmd, output_file=None):
    try:
        logger.debug(f"Command is running:{''.join(cmd)}")
        if output_file:
            with open(output_file, "w") as out:
                subprocess.run(cmd, stdout=out, check=True, stderr=subprocess.PIPE, text=True)
        else:
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"COMMAND ERROR: {''.join(cmd)}")
        logger.error(f"ERROR MESSAGE: {e.stderr}")
        raise

def run_pipeline(fastq, ref, output_dir):
    logger.info("--- NGS Pipeline is Started ---")

    output_path = Path(output_dir)
    output_path.mkdir(partents=True, exist_ok=True)
   
    sam_file = output_path / "aligned.sam"
    bam_file = output_path/"aligned.bam"
    sorted_bam = output_path/"aligned_sorted.bam"
    pileup_file = output_path/"pileup.vcf"
    vcf_file = output_path/"variants.vcf"
   

    try:
        
        logger.info("Step 1: Running aligment now...")
        run_command(["bwa", "mem", ref, fastq], str(sam_file))

        logger.info("Step 2: SAM file is converting to BAM format...")
        run_command(["samtools", "view", "-b", str(sam_file)], str(bam_file))

        logger.info("Step 3: Running sorting BAM now...")
        run_command(["samtools", "sort", "-o", str(sorted_bam), str(bam_file)] )

        logger.info("Step 4: Converting SAM to BAM now...")
        run_command(["bcftools", "mpileup", "-f", ref, str(sorted_bam)], str(pileup_file))
        run_command(["bcftools", "call", "-mv", "-Ov", str(pileup_file)], str(vcf_file))

        logger.info("--- Pipeline completed successfully! ---")
        logger.info(f"Results are here: {output_dir}")

    except Exception as e:
        logger.critical(f"PIPELINE IS STOP: There is an unexpected error: {e}")


       
