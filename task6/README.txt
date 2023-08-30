
About the files:
combine_test is a directory of files contains Bik dataset - papers with endpoint reached.tsv(the original Bik dataset), updated_bik_with_features.csv(datasets combined after task4 and task5)and three new datasets with different MIME types: Colleges_and_Universities.csv, NSF-metadata.xlsx and QSrank.txt. 
jaccard_similarity.py, edit-value-similarity.py, cosine_similarity.py and vector.py are downloaded from https://github.com/chrismattmann/tika-similarity.

Since the python version I use different from the github, I change the code in three py files: with open(outCSV, "wb") as outF to with open(outCSV, "w") as outF. If not, will meet an error: TypeError: a bytes-like object is required, not 'str'


To run the code for similarity, the pre-requisite is:

         1. Install Tika-Python
         2. Install Java Development Kit
         3. Download jaccard_similarity.py, edit-value-similarity.py and cosine_similarity.py from https://github.com/chrismattmann/tika-similarity.

How to run in the terminal:
         1. For Jaccard similarity, type:
         >>>python jaccard_similarity.py --inputDir combine_test --outCSV jaccard_similarity_output.csv
         
         you will get a csv called jaccard_similarity_output.csv contains details of jaccard similarity between different MIME type files.
         2. For Cosine Distance, type:
         >>>python cosine_similarity.py --inputDir combine_test --outCSV cosine_similarity_output.csv
         
         you will get a csv called cosine_similarity_output.csv contains details of cosine similarity between different MIME type files.
         3. For edit similarity, type:
         >>>python edit-value-similarity.py --inputDir combine_test --outCSV edit_distance_output.csv
         
         you will get a csv called edit_distance_output.csv contains details of cosine similarity between different MIME type files.
         
   