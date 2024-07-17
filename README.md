# ArqiSoft ez-assets-data-engg

Data Engineering Experiments for ez-assets.com.

This code will take a large Json file (encoding UTF-8 ) of Json objects and split it up into Json files that are less than 25 megabytes. 

It does this by reading your file and matching {} pairs and saving the data between them as a json object in an array.

The program will save any Json objects which cause a Json Decode Error into a separate folder.

Open the program in the same repository as your Json file to be split up.

## Run this in the terminal of the directory your data is in.

```terminal
python BracketMethod.py
```

Input the file path of your Json file to be split when prompted and the program will start. 

It will tell you as it finds problematic Json objects. 

Once it finishes parsing through the data it will inform you of the number of correctly parsed Json objects as well as the number of problematic json objects.

Then it will create a "Parsed_Json" folder that it will fill with Json files of Json objects that are all less than 25 megabytes from the array it created. It will then create "Problematic_Json" file composed of all the Json objects in your file that raised a Json Decode Error.
