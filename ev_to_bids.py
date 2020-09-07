#!/usr/bin/env python

'''
Constructs BIDS formatted TSV file from input FSL custom 3-column format stimulus files.

NOTE: This script is intended for the uncommon case in which the stimulus files were created from other means.
'''

# Import packages/modules
import sys
import pandas as pd

# Import packages/modules for argument parsing
import argparse

# Define functions
def fsl_stim_to_df(stim,trial_type="trial_type"):
    '''
    Constructs dataframe from FSL custom 3-column stimulus text file.
    
    Arguments:
        stim(file): FSL custom 3-column stimulus text file
        trial_type: Trial type/label
    Returns:
        df(df): Dataframe
    '''
    df = pd.read_csv(stim,header=None,sep="\t")
    df.columns = ["ONSET","DURATION","INTENSITY"]
    df['TRIAL_TYPE'] = f"{trial_type}"
    return df

def create_bids_df(*args):
    '''
    Constructs sorted dataframe from two or more input dataframes.
    The dataframes are sorted temporally by their 'ONSET' times.
    
    Arguments:
        *args: Two or more dataframes
    Returns:
        df(df): Concatenated and sorted dataframe
    '''
    frames = []
    for arg in args:
        frames+=[arg]
    df = pd.concat(frames,ignore_index=True)
    return df.sort_values(by=['ONSET'])

def create_bids_evs(**kwargs):
    '''
    Creates BIDS formatted EVs (explanitor variables) dataframe from
    input set of keyword arguments (or dict) consisting of 
    trial_labels/names and their corresponding FSL stimulus file.
    
    Arguments:
        **kwargs: Keyword paired arguments (or **dict)
    Returns:
        df(df): BIDS structured dataframe
    '''
    frames = []
    for key,value in kwargs.items():
        tmp_frame = fsl_stim_to_df(stim=value,trial_type=key)
        frames.append(tmp_frame)
    df = create_bids_df(*frames)
    return df.drop(["INTENSITY"],axis=1)

def create_bids_tsv(name_args,file_args,out="bids.tsv"):
    '''
    Constructs and writes output BIDS TSV file from input 
    FSL custom 3-column format stimulus files.
    
    Arguments:
        name_args(list): Name input list of stimuli name/label
        file_args(list): File input list of stimuli
        out(file): Output file name
    Returns:
        df(df): Output BIDS dataframe
        out(file): Output TSV
    '''
    # Check for equal length of input lists
    if len(name_args) != len(file_args):
        print("Input lists of stimulus and file names are of unequal length.")
        sys.exit(1)
    
    # Check output name
    if '.tsv' not in out:
        out = out + '.tsv'
        
    # Contruct data dictionary
    data = dict()
    for key,value in zip(name_args,file_args):
        tmp_dict = {key:value}
        data.update(tmp_dict)
        
    # Construct BIDS EVs (Explanitory Variables)
    df = create_bids_evs(**data)
    
    # Write BIDS TSV to file
    df.to_csv(out,sep="\t",index=False,header=True,mode="w")
    return df,out

def main():
    '''
    Main function.
    - Parses arguments
    - Executes parent function `create_bids_tsv`
    '''

    # Argument parser
    parser = argparse.ArgumentParser(description="Constructs BIDS formatted TSV file from input FSL-style custom 3-column " \
                                                 "format stimulus files. NOTE: the options '-s' and '-n' are repeatable.")

    # Parse Arguments
    # Required Arguments
    reqoptions = parser.add_argument_group('Required arguments')
    reqoptions.add_argument('-n', '--name',
                            type=str,
                            dest="name",
                            metavar="STR",
                            required=True,
                            action='append',
                            # nargs='+',
                            help="Name (label) of stimulus [Repeatable].")
    reqoptions.add_argument('-s', '--stimulus',
                            type=str,
                            dest="stim",
                            metavar="FILE",
                            required=True,
                            action='append',
                            # nargs='+',
                            help="Input stimulus file [Repeatable].")
    reqoptions.add_argument('-o', '--out',
                            type=str,
                            dest="out",
                            metavar="TSV",
                            required=True,
                            help="Output TSV (tab separated values) file to be written.")

    args = parser.parse_args()

    # Print help message in the case of no arguments
    try:
        args = parser.parse_args()
    except SystemExit as err:
        if err.code == 2:
            parser.print_help()

    [df,args.out] = create_bids_tsv(name_args=args.name,file_args=args.stim,out=args.out)

if __name__ == "__main__":
    main()