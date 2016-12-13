#!/usr/bin/env python

import boto3
import botocore
import argparse
import csv


def init_args():
    parser = argparse.ArgumentParser(
            description="Script for creating iam user")
    parser.add_argument("--csv", required=True, type=str,
                        help="Path for your csv file. Should following \
                        this format: Email, Password, Groups, Status. \
                        Multiple groups should be separated using ';'")
    parser.add_argument("--profile", required=False, type=str,
                        help="AWS profile credentials to be used")
    parser.add_argument("--region", required=False, type=str,
                        help="AWS region where the account resides")
    return parser.parse_args()


def init_iam_client(profile=None, region=None):
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client("iam")

    return client


def get_user(iam_client, username):
    try:
        response = iam_client.get_user(UserName=username)
        return response
    except botocore.exceptions.ClientError as e:
        if "NoSuchEntity" in e.message:
            return None
        print e.message


def create_user(iam_client, username, password, reset_password=True):
    try:
        user = get_user(iam_client, username)
        if not user:
            user = iam_client.create_user(UserName=username)
            iam_client.create_login_profile(
                    UserName=username,
                    Password=password,
                    PasswordResetRequired=reset_password)
    except botocore.exceptions.ClientError as e:
        print e.message


def attach_user_to_groups(iam_client, username, groups):

    for group in groups:
        try:
            iam_client.add_user_to_group(
                    GroupName=group,
                    UserName=username)
        except botocore.exceptions.ClientError as e:
            print e.message


def process_csv(iam_client, csv_name):
    with open(csv_name, "rb") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row["Status"] == "DONE":
                continue
            username = row["Email"].split("@")[0]
            password = row["Password"]
            groups = row["Groups"].split(";")

            create_user(iam_client, username, password)
            attach_user_to_groups(iam_client, username, groups)

            print username, groups


if __name__ == "__main__":

    args = init_args()

    iam_client = init_iam_client(profile=args.profile, region=args.region)
    process_csv(iam_client, args.csv)
