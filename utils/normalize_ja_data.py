import unicodedata
from tqdm import tqdm

from helpers import read_parallel_lines, write_lines


def normalize_text(text):
    text = unicodedata.normalize("NFKC", text)
    return text


def normalize_files(source_input, target_input, source_output, target_output, chunk_size=100000):
    source_data, target_data = read_parallel_lines(source_input, target_input)
    src_lines = []
    trg_lines = []
    count = 0
    for source_sent, target_sent in tqdm(zip(source_data, target_data)):
        source_sent = normalize_text(source_sent)
        target_sent = normalize_text(target_sent)
        src_lines.append(source_sent)
        trg_lines.append(target_sent)
        if len(src_lines) > chunk_size:
            count += len(src_lines)
            write_lines(source_output, src_lines, mode='a')
            write_lines(target_output, trg_lines, mode='a')
            src_lines = []
            trg_lines = []
    if src_lines:
        count += len(src_lines)
        write_lines(source_output, src_lines, mode='a')
        write_lines(target_output, trg_lines, mode='a')
    print("Normalize {}/{} lines".format(count, len(source_data)))
    print("Save source file to {}, target file to {}".format(source_output, target_output))


def main(args):
    normalize_files(
        source_input=args.src_in,
        target_input=args.trg_in,
        source_output=args.src_out,
        target_output=args.trg_out,
        chunk_size=args.chunk_size
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--src_in',
                        help='Path to the source file',
                        required=True)
    parser.add_argument('--trg_in',
                        help='Path to the target file',
                        required=True)
    parser.add_argument('--src_out',
                        help='Path to the output file',
                        required=True)
    parser.add_argument('--trg_out',
                        help='Path to the output file',
                        required=True)
    parser.add_argument('--chunk_size',
                        type=int,
                        help='Dump each chunk size.',
                        default=1000000)
    args = parser.parse_args()
    main(args)
