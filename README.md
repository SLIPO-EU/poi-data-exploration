# POI Data Exploration (PDE)

## Overview

PDE assists the user in obtaining an overview and insights about an unknown dataset.
A dataset usually consists of several fields and each could potentially contain a huge number of different values, numeric or string.
Conceptually, a dataset can be represented by a table, with a column for each field and the rows as the actual data.
In our current implementation, the input to PDE is a CSV file, with the first row defining the name of the fields, and each value separated from the others with a comma.

PDE can be used to extract insights regarding the entire dataset.
The user can retrieve basic information about the shape of the file (e.g., number of rows and number of columns) as well as information about the structure of the fields, e.g. which of them appear to be categorical, and in this case, which are their distinct values.

Moreover, when a specific field (column) is selected, more detailed information about the data contained in this field is computed and presented to the user.
This includes several common statistical parameters of the contained values, describing their distribution, as for example the mean value or the standard deviation in case the values are of numeric
type.
When dealing with strings, information such as the number of missing values, the number of unique values, their minimum and maximum length, the dominant value and its frequency, are computed.
Finally, for numeric types, the distribution parameters (or equivalently the distribution itself) is also computed to provide an overview of the data.

For the case of textual content, we perform a pattern analysis based on regular expressions.
First, the tool attempts to identify certain patterns in the input data, and subsequently to compute their frequencies.
In this way, the user is provided with a pattern distribution.
Each pattern reveals information about the nature of the characters contained in a string, for example if these are Latin or Greek words, numeric and their length, symbols, mixed concatenation of
characters, etc.
For each pattern, an example is given to be more comprehensible.
This case is considered as generic,
since the tool is yet completely agnostic about the nature of the data and performs a general analysis based on these identified patterns.

In addition, in the case of categorical data (i.e., when the values of a field are drawn from a relatively small set of distinct values), the tool is able to automatically identify these categories.
In fact, it is robust with respect to cases where each category may consist of several words and multiple categories are contained within each record.
Once these categories have been found and extracted, their frequency distribution inside the data is calculated and provided to the user.

Everything described so far is completely agnostic to the type of the specific field, which makes the tool more broadly useful and generally applicable to various types of data.
Nevertheless, since we focus on data concerning POI attributes, the analysis is made more specialized and optimized for field types which are frequently met.

Thus, in this specific analysis, the user can choose the type of the field under consideration. Specifically, the supported
field types are the following:

* name
* address
* phone number
* price range
* rating
* opening hours.

For the first three, we apply a predefined set of patterns. Instead of constructing the patterns from the data as in the generic case, this particular set of patterns is used, and as usual their frequency and finally their distribution is calculated.
These patterns have been designed to be as informative as possible for the specific field type.
For the rest of the supported field types, a different approach is followed since these field types are of numeric nature.
Once they have been stripped from any accompanying strings surrounding the numbers (the relative place of text and numbers, however, is taken into consideration), they are classified into appropriate bins, resulting in a distribution of the contained values.

## Execution

### Requirements

PDE is written in Python 3. Additionally, the following Python 3 libraries are required:

* [pandas](https://pandas.pydata.org/)
* [NumPy](http://www.numpy.org/)
* [re](https://docs.python.org/3/library/re.html)
* [collections](https://docs.python.org/3/library/collections.html)
* [unicodedata](https://docs.python.org/3/library/unicodedata.html)
* [json](https://docs.python.org/3/library/json.html)

### Running

In the command line run:

```bash
python explore.py filename=<dataset_file_container> [column=<column_to_analyze> [category=<generic|categorical|schedule|name|address|phone|rating> chart_type=<pie|bar>]]
```

If only filename is supplied, then the tool returns a JSON file with the general statistics of the dataset.
In order to compute more detailed statistics for a specific column, the name of the column has to be supplied in the parameter `column`.
In that case, the CSV file of the dataset has to include a first line with the column names.
The value passed to column has to coincide with one of these names.
If no other option is passed to the script, then a generic analysis is performed to the data contained inside this column.
Otherwise, in the case a `category` is supplied, the corresponding analysis is performed.


### Output

The results are returned in a JSON structure suitable in principle for generating, by default, a pie chart.
This can be altered by specifying the value of the parameter `chart_type` which can be either pie or bar.