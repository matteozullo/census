from typing import Dict
import geopandas as gpd
import us
from io import BytesIO

def pull_fips2state(fips2state=None):
    """
    Initialize fips to county dictionary adding back in areas not featured in original.
    """

    # Initialize dictionary
    if fips2state is None:
      fips2state = {state.fips: state.name for state in us.states.STATES}

    # Add District of Columbia
    fips2state['11'] = 'District of Columbia'
    fips2state['66'] = 'Guam'
    fips2state['69'] = 'Northern Mariana Islands'
    fips2state['60'] = 'American Samoa'
    fips2state['72'] = 'Puerto Rico'
    fips2state['78'] = 'U.S. Virgin Islands'
    return fips2state


def pull_fips2county(shapefile_url: str = 'https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip', full_countyname: bool = True) -> Dict[str, str]:
    """
    Retrieve a dictionary mapping FIPS codes to county names using Census shapefiles.

    Args:
        shapefile_url (str): URL to the Census shapefile containing county data.
        full_countyname (bool): Full name (True, default) or name (False) output.
          Full name is 'County, State' (e.g., "San Francisco County, California").
          Name is 'County' (e.g., "San Francisco").
    Returns:
        Dict[str, str]: A dictionary with FIPS code, county name pairs.
    """
    fips2state = pull_fips2state()
    try:
        # Load the county shapefile data
        counties = gpd.read_file(shapefile_url)

        # Check required columns
        required_columns = {'STATEFP', 'COUNTYFP', "NAME", "NAMELSAD"}
        if not required_columns.issubset(counties.columns):
            raise ValueError(f"Shapefile missing required columns: {required_columns - set(counties.columns)}")

        # Create a FIPS codes to county names dictionary
        fips2county = {}
        for idx, row in counties.iterrows():
          fips2county[f"{row['STATEFP']}{row['COUNTYFP']}"] = f"{row['NAMELSAD']}, {fips2state[row['STATEFP']]}"
        return fips2county

    #us.states.lookup(
    except Exception as e:
        raise RuntimeError(f"Error while retrieving FIPS-to-county mapping: {e}")


def pull_pep(file_url: str = "https://www2.census.gov/programs-surveys/popest/tables/2020-2023/counties/totals/co-est2023-pop.xlsx"):
    """
    Processe estimates from Census Bureau's Population Estimates Program (PEP).

    Returns:
        pd.DataFrame: County-level population data with FIPS codes.
    """

    # Download the XLSX file
    response = requests.get(file_url)
    response.raise_for_status()  # Ensure request was successful

    # Load into pandas
    df = pd.read_excel(BytesIO(response.content), skiprows=5, dtype=str)
    df.columns = ["geo", "2020_base", "2020", "2021", "2022", "2023"]

    # Drop rows with non-numeric values in population columns
    df = df[pd.to_numeric(df["2020_base"], errors='coerce').notna()]

    # Keep only relevant columns
    df = df[["geo", "2023"]]
    df.rename(columns={"2023": "pop"}, inplace=True)

    # Remove the initial '.' from "geo"
    df["geo"] = df["geo"].astype(str).str.lstrip('.')

    # Map to FIPS codes
    county2fips = {v: k for k, v in pull_fips2county().items()}
    df["county_fips"] = df["geo"].map(county2fips)

    return df
