'''
## Description of Program
- program:    tu3svi2_0bv1_sourcedatautility
- task:       Utility used across Social Vulnerability Index (SVI) to clean data
              main function renames variables to make comparisons easier
- Version:    2023-11-09
- 2024-03-26 - update with new SVI Dictionary column names 
- 2024-09-06 - Issue with how many decimal places to round to
- project:    DOE Southeast Texas Urban Field Lab SVI Paper - round 2 of analysis 
- funding:	  DOE
- author:    Nathanael Rosenheim
- GRA:        Lidia Mezei

File located in SourceData folder. Decided this was a good spot because 
this code mainly cleans up the source data and does not actually change 
any of the SVI data.
Use this program along with the following files:
- tu3svi2_0av1_SVIdatadictionary_2023-11-09.xlsx

As of 2023-11-09 this has been used in the following notebooks:
- UT_Preisser_SVI/tu3svi2_2av1_SetupUT_2023-11-09.ipynb
- www_atsdr_cdc_gov_placeandhealth_svi/tu3svi2_2bv1_SetupCDC_2023-11-09.ipynb
- texasatlas_arch_tamu_edu/tu3svi2_2cv1_SetupHRRC_2023-11-09.ipynb

This has been tested for the following SVI datasets:
- CDC ATSDR SVI 2018
- Hazard Redcution and Recovery Center (HRRC) SVI 2018
- University of Texas SVI 2018 from Matt Preisser
'''


import pandas as pd     # For obtaining and cleaning tabular data
import geopandas as gpd # For obtaining and cleaning spatial data
import numpy as np      # For working with arrays
import os # For saving to path

def update_varnames(varmetadata_df,
                    svi_name,
                    data_year,
                    merge_by_geo,
                    geoscales,
                    programname):
    """
    Code attempts to work through existing Social Vulnerability Index (SVI) data
    and update variable names to make comparisons easier.

    Code requires the following inputs:
    1. varmetadata_df: a dataframe containing the variable metadata 
                        these are from an Excel File
    2. svi_name: the name of the SVI (e.g. 'SVI2018')
    3. data_year: the year of the SVI (e.g. 2018)
    4. merge_by_geo: a dictionary containing the dataframes for each geoscale
    5. geoscales: a list of the geoscales (e.g. ['Tract', 'BG'])

    returns a dictionary of cleaned dataframes

    """
    # get unique values for varnames for CDC
    condition1 = varmetadata_df['SVI'] == svi_name
    condition2 = varmetadata_df['year'] == data_year
    varnames = varmetadata_df[condition1 & condition2]['oldvarname'].unique()

    # start dictionary to save cleaned files
    cleaned_files = {}
    for geoscale in geoscales:
        keep_vars = []
        df = merge_by_geo[geoscale].copy(deep=True)
        # loop over rows in dataframe
        for variable in varnames:
            current_varname = variable
            print("Current variable name: ", current_varname)
            # create new variable name
            condition1 = varmetadata_df['oldvarname'] == current_varname
            condition2 = varmetadata_df['year'] == data_year
            condition3 = varmetadata_df['SVI'] == svi_name
            var_metadata_row = varmetadata_df[condition1 & condition2 & condition3].copy(deep=True)
            # check if dataframe has data
            if len(var_metadata_row) == 1:
                print("Found variable in variable dictionary")
                # get the first letter of the SVI variable
                stem = var_metadata_row['SVI'].values[0][0]
                year = str(var_metadata_row['year'].values[0])
                order = str(var_metadata_row['order'].values[0])
                new_varname = stem + year + order

                # check if variable is the geocode
                if var_metadata_row['SVIcat'].values[0] == "Geocode":
                    common_category = str(var_metadata_row['comcat'].values[0])
                    new_varname = common_category

                print("Then new variable name is: ", new_varname, "check length: ", len(new_varname))
                # if converted to shapefiles they have a 10 character limit
                # rename variable
                # check if current varname is in df
                if current_varname in df.columns:
                    print("renaming", current_varname, "to", new_varname)
                    df = df.rename(columns={current_varname : new_varname})
                    # add variable to list of variables to keep
                    keep_vars.append(new_varname)

                    # check if variable is proportion or percentage
                    condition_percent = var_metadata_row['percent'].values[0] == 1
                    condition_not_proportion = var_metadata_row['proportion'].values[0] == 0
                    # check if percent is 1 and proportion is 0
                    if condition_percent & condition_not_proportion:
                        # print("converting", new_varname, "to proportion")
                        # divide by 100
                        df[new_varname] = df[new_varname] / 100
                    # set datatype
                    data_type = var_metadata_row['dtype'].values[0]
                    df[new_varname] = df[new_varname].astype(data_type)
                    if data_type == 'int64':
                        # round to the nearest 0th decimal place
                        df[new_varname] = df[new_varname].round(0)
                    if data_type == 'float':
                        # round to the nearest 5th decimal place
                        df[new_varname] = df[new_varname].round(5)
                else:
                    print("Could not find", current_varname, "in dataframe")
            elif len(var_metadata_row) > 1:
                print("Found multiple rows for variable in variable dictionary")
            else:
                print("Could not find", current_varname, "in variable dictionary")
        # save dataframe to dictionary
        cleaned_files[geoscale] = df[keep_vars].copy(deep=True)

        # Save Work as CSV
        print("Saving work as CSV")
        savefile = programname+"_"+geoscale+str(data_year)+".csv"
        cleaned_files[geoscale].to_csv(savefile, index=False)

    return cleaned_files

def quartileSVI(svi_df, quartile_prefix, svi_continuous_var):
    """
    Create a Comparable SVI with based on RPL_THEME Quartiles
    Arguments: SVI dataframe + SVI name appended to sviq variable in df + quartile variable name
    Function: Calculate quartiles using numpy & create a new categorical variable based on quartiles
    Returns: SVI dataframe
    """

    # copy svi_df
    df = svi_df.copy(deep=True)

    # Calculate quartiles using numpy.
    quartile_1 = df[svi_continuous_var].quantile(0.25)
    quartile_2 = df[svi_continuous_var].quantile(0.50)
    quartile_3 = df[svi_continuous_var].quantile(0.75)

    # Create a new categorical variable based on quartiles.
    quartiles = pd.cut(df[svi_continuous_var],
                    bins=[0, quartile_1, quartile_2, quartile_3, 1], 
                    labels=False)
    # Create integer labels - using 'Int64' to deal with NaNs
    df[quartile_prefix + '_sviq'] = quartiles.astype('Int64') + 1
    return df
