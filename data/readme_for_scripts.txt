we used the attricus dataset set master clause 
steps i did:

PRE-STEP:
a) use the 'for_size_sort.py' to add word count to the masterclause then you can easily sort the smaller files so that , 
   you can take the least size files , and then use add contract for those and feed to the llm to get the applicable laws ,
   else it will require lot of tokens


1) delete the extra columns, keep the imp ones only 
[Filename	Document Name	Parties	Agreement Date	Effective Date	Expiration Date	Renewal Term  Notice Period To Terminate Renewal	Governing Law	Exclusivity	Post-Termination Services]

b) use 'for_size_sort.py' to add a column which shows the word count then you can sort the contracts based on size, so that less tokens will be used to generate laws and train the model
c) after sorting delete the word count column as it is not required further

2) use 'for_contracts.py' which removes the .pdf extension from the filename column of dataset 
   and then iterates over it to extract the files from the folder which has the txt files with that name
   then it extract that data and put it in a new column in the dataset

3) change the "governing law" column to "governing law country" 

4) use 'fords.py' to generate names of applicable laws ( change the location as per your files, )
   you can also configure the prompt for that 

5) use 'for_exactlaw.py' to iterate over applicable laws names and get the summarized laws
