# app.library.inkscape_converter_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**convert_image_images_post**](DefaultApi.md#convert_image_images_post) | **POST** /images/ | Convert Image
[**get_health_async_health_async_get**](DefaultApi.md#get_health_async_health_async_get) | **GET** /health_async | Get Health Async
[**get_health_health_get**](DefaultApi.md#get_health_health_get) | **GET** /health | Get Health


# **convert_image_images_post**
> file_type convert_image_images_post(conversion_in)

Convert Image

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.http_validation_error import HTTPValidationError
from app.library.inkscape_converter_client.model.conversion_in import ConversionIn
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = app.library.inkscape_converter_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with app.library.inkscape_converter_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    conversion_in = ConversionIn(
        base64="base64_example",
        inputformat="inputformat_example",
        outputformat="outputformat_example",
    ) # ConversionIn | 

    # example passing only required values which don't have defaults set
    try:
        # Convert Image
        api_response = api_instance.convert_image_images_post(conversion_in)
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->convert_image_images_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **conversion_in** | [**ConversionIn**](ConversionIn.md)|  |

### Return type

**file_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_health_async_health_async_get**
> bool, date, datetime, dict, float, int, list, str, none_type get_health_async_health_async_get()

Get Health Async

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = app.library.inkscape_converter_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with app.library.inkscape_converter_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get Health Async
        api_response = api_instance.get_health_async_health_async_get()
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->get_health_async_health_async_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_health_health_get**
> bool, date, datetime, dict, float, int, list, str, none_type get_health_health_get()

Get Health

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = app.library.inkscape_converter_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with app.library.inkscape_converter_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get Health
        api_response = api_instance.get_health_health_get()
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->get_health_health_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

