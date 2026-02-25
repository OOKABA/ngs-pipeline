import gzip


def open_fastqa(path):
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    else:
        return open(path, "rt")


def count_read(path):
    line_count = 0

    with open_fastqa(path) as f:
        for _ in f:
            line_count += 1

    if line_count % 4 != 0:
        raise ValueError("Invalid FASTQ Format")
    return line_count // 4


def filter_read_by_gc(path, min_gc, max_gc):
    passed_reads = []
    line_counter = 0
    current_ID = None

    with open_fastqa(path) as f:
        for line in f:
            line_counter += 1
            line = line.strip()

            if line_counter % 4 == 1:
                current_ID = line[:]
            elif line_counter % 4 == 2:
                seq = line.upper()

                if len(seq) == 0:
                    continue
                gc_count = seq.count("G") + seq.count("C")
                gc_ratio = gc_count / len(seq)

                if min_gc <= gc_ratio <= max_gc:
                    passed_reads.append(current_ID)

    return passed_reads
