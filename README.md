# PolymerSelection
PolymerSelection is a tool that was designed in order to select the best possible polymer according to a set of target property values. The tool uses an algorithm that creates an internal test value to rank the different specimens closeness over all properties to their target value, giving the user a list of the closest matches. It is also able to select for any given property the closest specimens to that value. 

Though designed for usage with polymers in mind, with a small amount of tweaking, the code could be used for any number of data analysis uses where finding a specimen close to certain target values is desired. 

## System Requirements
PolmyerSelection runs simply on:
```
pandas 1.1.3 
```
though it will likely also work on earlier versions of pandas. 
