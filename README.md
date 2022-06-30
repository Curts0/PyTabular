
# PyTabular


### What Does It Do?

PyTabular allows for programmatic execution on your tabular models... In Python!

### How Does It Work?

I basically took my two favorite things Python and Tabular Models and connected the two. Thanks to [Pythonnet](https://pythonnet.github.io/) and Microsoft's [.Net APIs on Azure Analysis Services](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?view=analysisservices-dotnet). The package should have the dll files included when you import the package. 

### Getting Started

In your python environment, import pytabular and call the main Tabular Class. Only parameter needed is a solid connection string.

```python
    import pytabular
    model = pytabular.Tabular(CONNECTION_STR)
```

DAX Query

```python
    model.Query(DAX_QUERY)
```