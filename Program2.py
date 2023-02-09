"""
Name: Tenzing Nyima
Email: Tenzing.Nyima71@myhunter.cuny.edu
Resources: used pandas as reminder for panda functions.
Write a function that will drop extraneous columns and rename column names
so that they are the same, simplifying the subsequent function and analysis.
"""
import pandas as pd

def clean_df(df, year = 2015):
    """The function ddoes the following :
    if the specified year is 2015, the function should take df and drop all columns except:
    """
    if year == 2015:
        df = df.filter(items=['tree_dbh', 'health', 'spc_latin', 'spc_common', 'address',
        'zipcode','boroname','nta', 'latitude','longitude','council_district','census_tract'])
    elif year == 2005:
        df = df.filter(['tree_dbh', 'status', 'spc_latin', 'spc_common', 'address','zipcode',
        'boroname','nta','latitude', 'longitude','cncldist','census_tract'])
        df = df.rename(columns={'status':'health', 'cncldist':'council_district'})
    elif year == 1995:
        df = df.filter(['diameter', 'condition', 'spc_latin', 'spc_common', 'address',
        'zip_original','borough','nta_2010', 'latitude', 'longitude','council_district',
        'censustract_2010'])
        df = df.rename(columns={'diameter':'tree_dbh','condition':'health', 'zip_original':'zipcode',
        'borough':'boroname','nta_2010':'nta', 'censustract_2010':'census_tract'})

    return df

def filter_health(df, keep):
    """return data frame with rows that where the column health contains a value
    from list keep.All rows where the health column contains a different value
    are dropped."""
    rows = df[df['health'].isin(keep)]
    return rows

def add_indicator(row):
    """The function returns 1 if health is not Poor and tree_dbh is larger than 
    10 else it returns 0"""
    if row['health'] != 'poor':
        if row['tree_dbh'] > 10:
            return 1
    return 0

def find_trees(df, species):
    """The function should return , as a list, the address for all trees that species in spc_latin.
    If that species does not occur in the DAtaFrame, hten an empyt list is returned."""
    #species_address_list = []
    rows = df[df['spc_latin'] == species]
    species_address = []
    print(rows)
    for place in rows['address']:
        species_address.append(place)
    return species_address

def count_by_area(df, area="boroname"):
    """This function should return the sum of number of trees, grouped by area. For example if
    area == 'boroname', your function should group by boroname and return the number of
    each trees in each boroughs"""
    if area == "boroname":
        area_data = df[[area]].groupby(area).value_counts()
        count = area_data
    else:
        area_data = df[[area]].groupby(area).value_counts()
        count = area_data
    return count

def main():
    url ='https://data.cityofnewyork.us/resource/uvpi-gqnh.json?$limit=10000'
    data = pd.read_json(url)
    print(data)
    df = clean_df(data)
    print(f'The new columns are: {df.columns}.')
    url95 = 'https://data.cityofnewyork.us/resource/kyad-zm4j.json'
    data95= pd.read_json(url95)
    df95 = clean_df(data95, year = 1995)
    print(df95)
    df_h = filter_health(df, ['Fair','Good', 'Excellent'])
    healthy = 100*len(df_h)/len(df)
    print(f"In 2015, {healthy}% trees were healthy.")
    print(df.iloc[0])
    #print(df.iloc[0])
    print(f'First tree has indicator {add_indicator(df.iloc[0])}')
    df['Mature Trees'] = df.apply(add_indicator, axis=1)
    print(f"New column:\n {df['Mature Trees']}")
    print('American elm trees in our 2015 sample:')
    print(find_trees(df, "Ulmus americana"))
    print('In 2015, the number of trees by borough')
    print(count_by_area(df))
    print()
    print('In 2015, the number of trees by NTA')
    print(count_by_area(df, area = 'nta'))
if __name__ == "__main__":
    main()
