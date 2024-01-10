# PAC File Performance Comparer
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) [![GitHub license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/CACI-NS/pac-file-performance-comparer/blob/main/LICENSE)

## About
PAC File Performance Comparer is intended be run on an ad-hoc basis to allow a quick comparison using the [Pacparser](https://pacparser.manugarg.com) to calculate both the time difference (i.e. performance optimisation gain of the JavaScript PAC code refactor) and conformity against a test set of URL behaviours (i.e. proxy or direct) for a "before" and "after" PAC (Proxy Auto-Configuration File) refactoring exercise.

Modern websites and web applications often result in a large amount of simultaneous requests to a number of CDN, Static Hosting and other locations in order to load, so poorly-coded PAC files using multiple time-intensive functions such as `dnsDomainIs()`, `isResolvable()`, `dnsResolve()` and `isInNet()` can _significantly_ decrease performance of any applications which are PAC-aware.

The intent of this is to allow for a quick "before and after" benchmark of a PAC file rewriting exercise, with a resulting CSV output which aims to:
- Unit Test the expected behaviour of a URL (proxy or direct) against the processed behaviour (proxy... or direct) of a given "before" and "after" set of PAC files
- Display the PAC-processed behaviour of a URL (proxy or direct) of a given "before" and "after" set of PAC files
- Display the time taken by the browser engine to process the PAC to calculate the behaviour (proxy or direct) of a given "before" and "after" set of PAC files

Example CSV output for a run might look like:

| url | old_pac_action | old_pac_status | old_pac_timer_milliseconds | new_pac_action | new_pac_status | new_pac_timer_milliseconds |
| --- | -------------- | -------------- | -------------------------- | -------------- | -------------- | -------------------------- |
| bbc.co.uk | PROXY 2.2.2.2:8080 | pass | 1 | PROXY 2.2.2.2:8080 | pass | 1 |
| madeupapphere.internal-domain.company.com | DIRECT | pass | 1 | DIRECT | pass | 0 |
| oldappnotyetremoved.something-else-old.oldcompanyname.com | DIRECT | pass | 0 | DIRECT | pass | 0 |
| website3.com | PROXY 2.2.2.2:8080 | fail | 0 | DIRECT | pass | 0 |

## Requirements
- Python 2.7 or 3.4+
   - Pacparser

## Executables
| Name | Type | Run Order | Description |
| ---- | ---- | --------- | ----------- |
| compare.py | Python Script | First | Performs the comparison of the two specified PAC files |

## Inputs
| Name | Type | Example Input | Description |
| ---- | ---- | -------------- | ----------- |
| tests.csv | Text (CSV) | `google.com,proxy` | Expected behaviour for a given URL from a choice of `proxy` or `direct` |
| prod.pac | Text (PAC/JavaScript) | `function FindProxyForURL(url, host) {...}` | Original PAC file before refactoring for performance efficiency |
| prod_new.pac | Text (PAC/JavaScript) | `function FindProxyForURL(url, host) {...}` | Rewritten PAC file after refactoring for performance efficiency |


## Outputs
| Name | Type | Example Output | Description |
| ---- | ---- | -------------- | ----------- |
| output.csv | Test (CSV) | `url,old_pac_action,old_pac_status...` | Output result of Unit Tests and PAC processing time for each PAC file, compared against each other |

## Installation
### Download
Depending on whether your Network Management Jumpbox has Direct/Proxy Internet Access, either:
- Git clone this repo into the desired folder (i.e. assuming Linux OS, maybe into `/opt/scripts/pac-file-performance-comparer/`)
- Download this repo as a ZIP and unzip into the desired folder on your Network Management Jumpbox

The example `output.csv` file supplied will be overwritten on the first run of the script.

The example `prod.pac` and `prod_new.pac` files need to be overwritten with your specific PAC logic.

The example `tests.csv` file need to be overwritten with the URLs which can act as a full suite of Unit Tests against your specific PAC logic.

### Python Modules
The following PyPI Modules are required as per `requirements.txt`:
- Pacparser

Install these on the Network Management Jumpbox with:

`pip install -r requirements.txt`

### Environment Variables
All relevant locally-significant Environment Variables are stored within ALL_CAPS constants specified towards the top of each Python executable script, these will need to be modified prior to first-run to your specific Environment (i.e. your Company's specific name for the PAC file, or specific Installation Directory etc). The important Constants to change are:
| Script | Variable | Example | Description |
| ------ | -------- | ------- | ----------- |
| compare.py | INPUT_CSV | `tests.csv` | Filename of the CSV file containing the Unit Tests to run on each URL to check behaviour of |
| compare.py | OUTPUT_CSV | `output.csv` | Filename of the CSV file to contain the results of the side-by-side PAC comparison testing |
| compare.py | OLD_PAC | `prod.pac` | Filename of the original PAC file before refactoring |
| compare.py | NEW_PAC | `prod_new.pac` | Filename of the rewritten PAC file after refactoring for performance optimisation |

Other Constants are also commented within the Python executable scripts themselves, if required to be changed for your specific Environment.

## Scheduling
This script is designed to be run ad-hoc as and when needed to generate evidence for the relevant PAC file performance comparison.

## Resources
* [Example PAC File from FindProxyForURL](https://findproxyforurl.com/example-pac-file/)
* [PAC Functions from FindProxyForURL](https://findproxyforurl.com/pac-functions/)
* [Forcepoint PAC file best practices](https://www.websense.com/content/support/library/web/v76/pac_file_best_practices/PAC_best_pract.aspx)
* [Pacparser library to parse proxy auto-config (PAC) files](https://pacparser.manugarg.com)