# Author: AAnkers
# Date: 10-Jan-2024
# Description: Compare two PAC files for performance and URL behaviour conformance
import logging
import pacparser
import time

from utils import get_formated_time, write_csv, read_csv, PACTest

# Define Constants
INPUT_CSV: str = "test.csv"  # Filename of the input CSV file (informs the PAC Tester what expected behaviour, proxy or direct, is per URL; header format: url,expected_action)
OUTPUT_CSV: str = "output.csv"  # Filename of the output CSV file
OLD_PAC: str = "prod.pac"  # Filename of the first input PAC file (old pre-optimised version)
NEW_PAC: str = "prod_new.pac"  # Filename of the second intput PAC file (new optimised version)


def pac_test(url: str, pac_file: str) -> PACTest:
    start_time = time.time()

    pacparser.init()
    pacparser.parse_pac(pac_file)
    pacparser.setmyip("10.0.0.1")
    result = pacparser.find_proxy("https://" + url, url)

    end_time = time.time()
    elapsed_time = int((end_time - start_time) * 1000)

    pacparser.cleanup()

    return PACTest(
        result=result,
        elapsed_time=elapsed_time
    )


def main() -> None:
    logging.info(f'JOB START: {get_formated_time()}\n')

    # Open Tests CSV file, begin processing
    logging.info(f'Processing and comparing PAC file ["{OLD_PAC}"] against PAC file ["{NEW_PAC}"]...')

    field_names: list[str] = [
        "url",
        "old_pac_action",
        "old_pac_status",
        "old_pac_timer_milliseconds",
        "new_pac_action",
        "new_pac_status",
        "new_pac_timer_milliseconds"
    ]

    output: str = ''

    try:
        csv_reader: list[dict] = read_csv(filename=INPUT_CSV)

        for row in csv_reader:
            # Test against old PAC
            test_old: PACTest = pac_test(row.get("url"), OLD_PAC)
            status_old: str = "pass" if row.get("expected_action").lower() in test_old.result.lower() else "fail"

            # Test against new PAC
            test_new: PACTest = pac_test(row.get("url"), NEW_PAC)
            status_new: str = "pass" if row.get("expected_action").lower() in test_new.result.lower() else "fail"

            logging.info(f'Entry: {row.get("url")} should go via: {row.get("expected_action")}, '
                         f'old PAC goes via: {test_old.result}, new PAC goes via: {test_new.result} '
                         f'[Old PAC Processing: {str(test_old.elapsed_time)}ms, '
                         f'New PAC Processing: {str(test_new.elapsed_time)}ms]')

            # Add to output string
            output += f'{row.get("url")},{test_old.result},{status_old},{test_old.elapsed_time},{test_new.result},{status_new},{test_new.elapsed_time}'

        logging.info(f"Writing output CSV to file: {OUTPUT_CSV}...")
        write_csv(filename=OUTPUT_CSV, field_names=field_names, data=output)
        logging.info("Write File Success")

    except Exception as e:
        logging.error(f"Error: {str(e)}")

    finally:
        logging.info(f"JOB END: {get_formated_time()}")


if __name__ == '__main__':
    main()
