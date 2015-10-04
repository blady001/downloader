# downloader

What is it?
-----------
Downloader is a simple python script for manually specifying file types that user wants to download from github. 
One can for example download only contents of the "contents" directory without downloading whole project or each file 
separately. It is most useful in case of large assets directories (like in many tutorial repositories).

Usage
-----
Simply run main.py script, it will prompt you to pass url to the desired repo and (optionally) specify file types. 
Pay attention:
 - Please make sure that 'downloads' folder is in the script's direcotory. It is a place where downloaded files are stored.
 - The default behavior is that script searches for files not only in a repo's directory passed from link but also in all 
 subdirs of the that directory, i.e. it tries to fetch ALL files with a given extension. For now it is unresolved.
