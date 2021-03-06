# create_iam_user

This script intended to automatically create iam_user in any account in AWS. Currently it's only supporting csv file format and will be updated in the near future

# How to Install

* Clone this repository
* Execute the script

# How to use
```
usage: iam_user.py [-h] --csv CSV [--profile PROFILE] [--region REGION]

Script for creating iam user

optional arguments:
  -h, --help         show this help message and exit
  --csv CSV          Path for your csv file. Should following this format:
                     Email, Password, Groups, Status
  --profile PROFILE  AWS profile credentials to be used
  --region REGION    AWS region where the account resides
```

# Example
## CSV File
Below example will insert new user with someone as its username and changemeplease as the password
```
Email,Password,Groups,Status
someone@gmail.com,changemeplease,group;group1,
```

The script will not reexecute the user creation if the status marked as done
```
Email,Password,Groups,Status
someone@gmail.com,changemeplease,group;group1,DONE
```

## Command Line
```./iam_user.py --csv ~/Downloads/a.csv --profile dev --region ap-southeast-1```
