import json
import yaml
import argparse
import logging
import pandas as pd


logger = logging.getLogger("monies")
logger_format = logging.Formatter('monies.py - %(levelname)s: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logger_format)
logger.addHandler(stream_handler)


def calculate_shares(
        expenses: pd.DataFrame,
        ratios: dict[str, float] = None
) -> pd.DataFrame:

    names = expenses["name"].unique()
    logger.info(f"calculating shares for {', '.join(names)}")

    if ratios is None:
        ratios = {n: 1 for n in names}

    logger.debug(f"ratios of shares is {json.dumps(ratios, indent=4)}")

    total = expenses["amount"].sum()
    logger.info(f"spent total: {total:.2f}")

    info = dict()
    for name in names:
        ratio = ratios[name] / sum(ratios.values())
        share = ratio * total
        paid = expenses[expenses["name"] == name]["amount"].sum()
        still_open = share - paid
        logger.info(f"-- {name:10} --")
        logger.info(f"  share: {share:.2f}")
        logger.info(f"  open:  {still_open:.2f}")

        info_name = {
            "ratio": ratio,
            "share": share,
            "paid": paid,
            "open": still_open
        }

        info[name] = info_name

    result = pd.DataFrame.from_dict(info, orient="index")
    logger.debug("\n" + result.to_string())
    return result


def load_config(
        config_filename: str
) -> dict:
    logger.info(f"loading {config_filename}")

    with open(config_filename, "r") as f:
        config = yaml.safe_load(f)

    name = config["name"]
    logger.info(f"reading {config['infile']}")
    expenses = pd.read_csv(config["infile"])
    logger.debug("\n" + expenses.to_string())
    outfile_name = config["outfile"]
    ratios = config.get("ratios")

    config_dict = dict(
        name=name,
        expenses=expenses,
        outfile_name=outfile_name,
        ratios=ratios
    )

    return config_dict


def main(
        config_filename: str
):
    config_dict = load_config(config_filename)
    shares = calculate_shares(config_dict["expenses"], config_dict["ratios"])
    logger.debug(f"saving to {config_dict['outfile_name']}")
    shares.to_csv(config_dict["outfile_name"])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="path to config file")
    parser.add_argument("-l", "--logging-level", type=str, default="INFO", help="logger level")
    args = parser.parse_args()
    logger.setLevel(args.logging_level)
    main(args.config)
