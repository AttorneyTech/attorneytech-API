# OpenAPI/Swagger Style Guide ![openapi](https://img.shields.io/badge/openapi-3.0-green.svg)

This is a style guide for writing code in OpenAPI/Swagger using YAML for this project.

## Filter Query Parameters

Query parameters used for filtering data should appear in the following form:
* `filter[<field>]=<value>`: if `field` and `value` are both a single value and the filter checks for \
  strict equality
* `filter[<field>][<operation>]=<value>`: otherwise

`field` is a semantic name for the field being used to filter the resources. If the field
corresponds to an `attribute` of the resource, it should be named after this attribute if possible.
`operation` refers to the operation being applied to filter the resources.

Below is a list of allowed values for `operation`

| `operation` | Description                                    |
| ----------- | ---------------------------------------------- |
| `neq`       | Not equal to                                   |
| `gt`        | Greater than                                   |
| `gte`       | Greater than or equal to                       |
| `lt`        | Less than                                      |
| `lte`       | Less than or equal to                          |
| `oneOf`     | `field` is one of the following                |
| `noneOf`    | `field` is none of the following               |
| `hasSome`   | `field` contains at least one of the following |
| `hasAll`    | `field` contains all of the following          |
| `hasNone`   | `field` contains none of the following         |
| `fuzzy`     | `value` partially matches `field`              |

### Examples

* `filter[name]=Saul` - Matches all resources with name "Saul"
* `filter[name][oneOf]=Saul,Kimberley,Howard` - Matches all resources with name "John", "Kimberley", or "Howard"
* `filter[name][fuzzy]=Sa` - Matches all resources whose name partially equals "Sa" such as "Sa",
  "Saul", or "Sam"
* `filter[courtDate][lte]=date-time` - Matches all resources with the court date is less than date-time input
* `filter[courtIds][hasSome]=1,2` - Matches all resources that courtIds is 1 or 2
