# app.library.inkscape_converter_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_image_images_image_id_delete**](DefaultApi.md#delete_image_images_image_id_delete) | **DELETE** /images/{image_id} | Delete Image
[**download_image_images_image_id_download_get**](DefaultApi.md#download_image_images_image_id_download_get) | **GET** /images/{image_id}/download | Download Image
[**get_health_async_health_async_get**](DefaultApi.md#get_health_async_health_async_get) | **GET** /health_async | Get Health Async
[**get_health_health_get**](DefaultApi.md#get_health_health_get) | **GET** /health | Get Health
[**get_image_images_image_id_get**](DefaultApi.md#get_image_images_image_id_get) | **GET** /images/{image_id} | Get Image
[**get_images_images_get**](DefaultApi.md#get_images_images_get) | **GET** /images/ | Get Images
[**post_image_images_post**](DefaultApi.md#post_image_images_post) | **POST** /images/ | Post Image


# **delete_image_images_image_id_delete**
> bool, date, datetime, dict, float, int, list, str, none_type delete_image_images_image_id_delete(image_id)

Delete Image

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.http_validation_error import HTTPValidationError
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
    image_id = "image_id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete Image
        api_response = api_instance.delete_image_images_image_id_delete(image_id)
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->delete_image_images_image_id_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **image_id** | **str**|  |

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
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_image_images_image_id_download_get**
> file_type download_image_images_image_id_download_get(image_id)

Download Image

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.http_validation_error import HTTPValidationError
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
    image_id = "image_id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Download Image
        api_response = api_instance.download_image_images_image_id_download_get(image_id)
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->download_image_images_image_id_download_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **image_id** | **str**|  |

### Return type

**file_type**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
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

# **get_image_images_image_id_get**
> ConversionResponse get_image_images_image_id_get(image_id)

Get Image

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.http_validation_error import HTTPValidationError
from app.library.inkscape_converter_client.model.conversion_response import ConversionResponse
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
    image_id = "image_id_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Image
        api_response = api_instance.get_image_images_image_id_get(image_id)
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->get_image_images_image_id_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **image_id** | **str**|  |

### Return type

[**ConversionResponse**](ConversionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_images_images_get**
> [ConversionResponse] get_images_images_get()

Get Images

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.conversion_response import ConversionResponse
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
        # Get Images
        api_response = api_instance.get_images_images_get()
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->get_images_images_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ConversionResponse]**](ConversionResponse.md)

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

# **post_image_images_post**
> ConversionResponse post_image_images_post(conversion_request)

Post Image

### Example

```python
import time
import app.library.inkscape_converter_client
from app.library.inkscape_converter_client.api import default_api
from app.library.inkscape_converter_client.model.http_validation_error import HTTPValidationError
from app.library.inkscape_converter_client.model.conversion_request import ConversionRequest
from app.library.inkscape_converter_client.model.conversion_response import ConversionResponse
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
    conversion_request = ConversionRequest(
        base64="base64_example",
        input_format="input_format_example",
        output_format="output_format_example",
    ) # ConversionRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Post Image
        api_response = api_instance.post_image_images_post(conversion_request)
        pprint(api_response)
    except app.library.inkscape_converter_client.ApiException as e:
        print("Exception when calling DefaultApi->post_image_images_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **conversion_request** | [**ConversionRequest**](ConversionRequest.md)|  |

### Return type

[**ConversionResponse**](ConversionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

