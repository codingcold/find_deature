Description: For part 5 of the tasks, in order to get the dataset which is high related to Bik Dataset (Bik dataset - papers with endpoint reached.tsv),
I have created one ipython file named task_5.ipynb to add some features of our finding of three datasets (NSF-metadata.xlsx, Colleges_and_Universities.csv and QSrank.txt) 
from the folder named 3datasets into updated_bik.csv(the data is updated after task4, which can be later named as updated_bik_with_fearures.csv.)
As for task_5.ipython, I first identify these features in one xlsxl file named NSF-metadata.xlsx: 'DOI', 'Title', 'Creator/Author', 'Journal Name', 'Sponsoring Org.'; 
then I identify these attributes in a csv file named Colleges_and_Universities.csv:'NAME','ADDRESS','STATE','COUNTRY','COUNTY','SOURCE','WEBSITE'; and I finally labeled 
first three columns from this dataset called QSrank.txt as 'UNI_RANKS', 'UNI_NAMES', and 'UNI_AREAS' and identify these
data from first three columns. By identifying the features of all these data, I add them into updated_bik.csv which can be later titled as updated_bik_with_fearures.csv.

Requirements: 
Following requirements are needed to be satisfied to run all the codes:
Packages to be installed:
1.tika
2.pandas
3.openpyxl
To install above packages use the following command: pip install + any package, like pip install tika, 
pip install pandas, and pip install openpyxl.


Data Sources:
1.NSF Public Access Repository(data scource: https://catalog.data.gov/dataset/nsf-public-access-repository)
data link: https://par.nsf.gov/search/term:PLOS
I type 'PLOS' in the data link from the link of data scource to download xlsx the dataset NSF-metadata.xlsx 
which is related to PLOS, and will use these features: DOI', 'Title', 'Creator/Author', 'Journal Name', and 'Sponsoring Org.',
simply because the first 48 rows of BIk data's articles are from PLOS with each article's authors, title, and DOI, therefore, 
I just wonder if the extracting features from this xlsx is highly related to Bik Dataset.

2. Colleges and Universities(data scource https://catalog.data.gov/dataset/colleges-and-universities-76556)
data link: https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::colleges-and-universities/explore?location=2.988708%2C43.985176%2C1.58
I just download the csv directly from data link which is from the link of data scource, and will use these features:'NAME','ADDRESS',
'STATE','COUNTRY','COUNTY','SOURCE','WEBSITE' in the code task_5.ipython, mainly because the extracting features are highly related 
to the university which can be connected to the added additional feature for Bik Dataset:first Author's Affiliation University, 
in the end, there exists the possibility that there is correlations between these extracting features and the scrapped feature:
first Author's Affiliation University.

3.World University Rankings(https://www.kaggle.com/datasets/mylesoneill/world-university-rankings)
I extract data from first three columns of this txt dataset and name these columns as 'UNI_RANKS','UNI_NAMES', and 'UNI_AREAS' 
respectively.


Running the code file named task_5.ipython:
I just run the file cell by cell directly to get updated_bik_with_fearures.csv..